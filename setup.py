# -*- coding:Utf-8 -*-

from setuptools import setup

from wargod import __version__

setup(name='wargod',
      version=__version__,
      description='river flow type minimaliste rss reader that generate static html pages ',
      author='Laurent Peuch',
      long_description=open("README").read(),
      author_email='cortex@worlddomination.be',
      url='https://github.com/Psycojoker/wargod',
      install_requires=['beautifulsoup', 'lxml', 'feedparser', 'yaml', 'jinja2'],
      packages=['wargod'],
      license= 'aGPLv3+',
      # list of scripts supplied by your application
      scripts=['bin/wargod'],
      keywords='rss atom reader static html',
     )

# vim:set shiftwidth=4 tabstop=4 expandtab:
