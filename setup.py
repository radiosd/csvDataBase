#!usr/bin/env python
"""
    setup for rgrCsvData,
    The library package for access to csv files as a database.
                                                        23jun18
"""

from distutils.core import setup

VERSION_FILE = 'rgrCsvData/version.py'
# read version and other information from the package
version = {}
with open(VERSION_FILE) as fin:
    exec(fin.read(), version)

setup(name='rgrCsvData',
      version = version['__version__'],
      description = 'The library package for access to csv files as a database',
      author = 'Richard Ranson',
      scripts = [],
      packages = ['rgrCsvData']
      )

