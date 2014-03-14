#!/usr/bin/env python
import json
import os
import pprint

import cherrypy
import requests
from simplejson import JSONEncoder

from config import configTmModules
from tm_modules import TeamDashboardGraph

encoder = JSONEncoder()
oDebugPrint = pprint.PrettyPrinter(indent=2)

def jsonify_tool_callback(*args, **kwargs):
  response = cherrypy.response
  response.headers['Content-Type'] = 'application/json'
  response.headers['Access-Control-Allow-Origin'] =  '*';

cherrypy.tools.jsonify = cherrypy.Tool('before_finalize', jsonify_tool_callback, priority=30)

class TeamDashboardData(object):


  MAX_HISTORY = 1000

  def __init__(self):
    self._dReviews = {}
    self._iCpt = 0

  @cherrypy.expose
  def index(self, value_path=None):
    return self.sHelpHtml

  ######################################################################
  #
  # Gerrit
  #
  ######################################################################
  #TODO: move it in tm_modules

  sHelpGerritModule = """
  <h2>Gerrit Module</h2>
  <ul>
    <li>Graph or count reviews on gerrit.</li>
  </ul>

  <h3>Link to the dashboard tool</h3>
  <ul>
    <li><a href="http://fdietz.github.io/team_dashboard/">Project page</a></li>
  </ul>

  <h3>List of available urls</h3>
  <ul>
    <li> /gerrit?user=YOUR_USER <br />
          <span style="margin: 0 0 0 25px;">- nb reviews for a user</span>
    </li>
    <li> /getOpenByProduct/?product1=repo1,repo2&product2=repo1,repo3 <br />
          <span style="margin: 0 0 0 25px;">- get one graph by product</span>
    </li>
  </ul>
  """

  def getReviewListFromAnswer(self, poAnswer):
    return json.loads(poAnswer.content.replace(")]}'", ""))

  @cherrypy.expose
  @cherrypy.tools.jsonify()
  def gerrit(self, user):
    lsUrl = '%s/changes/?q=status:open+owner:%s' % (configTmModules.GIT_URL, user)
    ldHeaders = {'Content-Type': 'application/json'}
    loAnswer = requests.get(lsUrl, headers=ldHeaders)
    llReviews = json.loads(loAnswer.content.replace(")]}'", ""))
    lsUrl = '%s/changes/?q=status:open+reviewer:%s' % (configTmModules.GIT_URL, user)
    loAnswer = requests.get(lsUrl, headers=ldHeaders)
    llToReview = json.loads(loAnswer.content.replace(")]}'", ""))
    return json.dumps({'mine': len(llReviews), 'to_review': len(llToReview)})

  def _getOpenProjects(self, psProductName, plProjects, graph=None, **args):

    liNbReview = len(self._getOpenFromProjectList(plProjects))
    if graph == None:
      return json.dumps({'count': liNbReview})
    else:
      if psProductName not in self._dReviews:
        self._dReviews[psProductName] = TeamDashboardGraph(psProductName, self.MAX_HISTORY)
      self._dReviews[psProductName].addPoint(liNbReview)
      print self._dReviews[psProductName].getResult()
      return (self._dReviews[psProductName].getResult())

  @cherrypy.expose
  @cherrypy.tools.jsonify()
  def getOpenByProduct(self, **pdArgs):
    llProductsGraphData = []
    for lsProductName in pdArgs:
      llRepos = pdArgs[lsProductName].split(',')
      llProductsGraphData.append(self._getOpenProjects(lsProductName, llRepos, True))

    return json.dumps(llProductsGraphData)


  def _getOpenFromProjectList(self, plProjects):
      llResults = []
      ldHeaders = {'Content-Type': 'application/json'}
      for lsProject in plProjects:
        lsUrl = '%s/changes/?q=status:open+project:%s' % (configTmModules.GIT_URL, lsProject)
        loAnswer = requests.get(lsUrl, headers=ldHeaders)
        for ldResult in self.getReviewListFromAnswer(loAnswer):
          llResults.append(ldResult)
      return llResults


  ######################################################################
  #
  # Homepage
  #
  ######################################################################

  sHelpHtml = """
  <h1>Team Dashboard data</h1>
  <p>This is an rough JSON api for Team Dashboard to plug different api on it.</p>

  """
  sHelpHtml += sHelpGerritModule

  @cherrypy.expose
  def index(self, value_path=None):
    return self.sHelpHtml


def main():
  cherrypy.config.update({
      'server.socket_port': configTmModules.PORT,
      'server.socket_host': configTmModules.NETWORK_LISTENED,
      'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
      'tools.decode.on': True,
      'tools.trailing_slash.on': True,
      'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),
  })

  cherrypy.quickstart(TeamDashboardData(), '/', {})


if __name__ == '__main__':
    main()
