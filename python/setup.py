#!/usr/bin/env python
#pyencrypt:disable
from __future__ import with_statement
from distutils import log, dir_util
import os
import re
import time
import sys
import urllib
from setuptools import setup, find_packages
from setuptools.command import sdist as _sdist
import subprocess


DEVELOPEMENT_VERSION = True
VERSION = "1.0.0"

# @see:
#  http://packages.python.org/distribute/setuptools.html#specifying-your-project-s-version
# for defails about post/pre release tags.
if DEVELOPEMENT_VERSION is True:
  post_release_tag = time.strftime('r%Y%m%d')
  VERSION = '-'.join([VERSION, post_release_tag])

DEV_DEPENDENCIES = [
            'nose>=0.11.1',
         ]

class SdistCryptCommand(_sdist.sdist):
  """This command replaces sdist standard command
    and encrypts source distribution."""

  ENCRYPT_SUFFIXES = [ '.py' ]
  DISABLE_ENCRYPT_PATTERN = "\s*#\s*pyencrypt:\s*disable"

  def _getEncryptCommand(self):
    lsPlatformFolder = "Linux-x64"
    if sys.platform.startswith('win'):
      lsPlatformFolder = "Windows-x64"
    return os.path.join(os.path.expandvars('$TEAMPDV'), "builds",
                        "Python-crypted-2.7.3", lsPlatformFolder, "pyencrypt")

  def make_release_tree(self, psBaseDir, plFiles):
    """Override standard make_release_tree method
      in order to encrypt .py files found.

      This method is a rewrite of distutils.command.sdist
      make_release_tree method but don't create hard link because
      we don't want do modify source files.

      ditribute.command.sdist method is not called because it
      wrap distutils.command.sdist method in order to not create
      hard link on setup.cfg in order to keep the original unmofieid.
      Our re-write achieve the same goal.

    """
    self.mkpath(psBaseDir)
    dir_util.create_tree(psBaseDir, plFiles, dry_run = self.dry_run)
    loRegex = re.compile(self.DISABLE_ENCRYPT_PATTERN)
    for lsFile in plFiles:
      if os.path.isfile(lsFile):
        lsDst = os.path.abspath(os.path.join(psBaseDir, lsFile))
        self.copy_file(lsFile, lsDst)
        if os.path.splitext(lsFile)[1] in self.ENCRYPT_SUFFIXES:
          with open(lsFile, "r") as loFd:
            if loRegex.search(loFd.read()):
              continue
          liReturn = subprocess.call([self._getEncryptCommand(), lsDst])
          if liReturn != 0:
            raise IOError("Can't encrypt %s." % lsDst)
    self.distribution.metadata.write_pkg_info(psBaseDir)
    self.get_finalized_command('egg_info')\
        .save_version_info(os.path.join(psBaseDir, 'setup.cfg'))


PARAMETERS = {
  'name': 'dashboard-data-server',
  'description': "LTU Dashbaord data server package.",
  'author': "LTU Technologies - Arnaud Lamy",
  'author_email': "alamy@ltutech.com",
  'maintainer': "LTU Technologies",
  'maintainer_email': "alamy@ltutech.com",
  'cmdclass': { 'sdist_crypt': SdistCryptCommand },
  'license': "PRIVATE",
  'test_suite': "nose.collector",
  'include_package_data': True,
  'setup_requires': ['nose>=0.11.1'],
  'version': VERSION,
  'zip_safe': False,
  'dependency_links' : [
    '://'.join(['file', urllib.pathname2url(os.path.join(os.path.abspath(os.path.dirname(__file__)),"dist"))])
  ],
  'entry_points': {
    'console_scripts': [
        ]
  },
  'packages': find_packages(),
  'package_dir': {
  },
  'namespace_packages': [],
  'install_requires': [ 'cherrypy', 'simplejson', 'requests' ],
  'tests_require': DEV_DEPENDENCIES
}

if __name__ == "__main__":
  setup(**PARAMETERS)
