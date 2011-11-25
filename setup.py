# -*- coding:Utf-8 -*-

from setuptools import setup

from wargod import __version__

setup(name='wargod',
      version=__version__,
      description='FIXME',
      author='FIXME',
      long_description='FIXME',
      # or you can also do something like this
      # long_description=open("README").read(),
      author_email='FIXME',
      url='FIXME',
      # install_requires=['lib_with_a_certain_version>=0.9.9.1', 'another_lib'],
      # list of packages you want you application/lib install
      packages=['wargod'],
      license= 'FIXME',
      # list of scripts supplied by your application
      scripts=['bin/wargod'],
      keywords='FIXME',
     )

# vim:set shiftwidth=4 tabstop=4 expandtab:
