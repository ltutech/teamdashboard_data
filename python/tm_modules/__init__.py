import calendar
from datetime import timedelta, datetime, date


class TeamDashboardGraph(object):

  def __init__(self, psName, piMaxPoints):
    self._iMaxNbPoint = piMaxPoints
    self._lPoints = []
    self._dTDReturn = { 'target': psName, 'datapoints': self._lPoints }

  def addPoint(self, piValue, piTimestamp=None):
    if not piTimestamp:
      liTimestamp = calendar.timegm(datetime.utcnow().utctimetuple())
    else:
      liTimestamp = piTimestamp
    if len(self._lPoints) == self._iMaxNbPoint:
      self._lPoints.pop(0)
    self._lPoints.append([piValue, liTimestamp])

  def getResult(self):
    return self._dTDReturn
