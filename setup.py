#!/usr/bin/env python3

from distutils.core import setup

setup(name='Inceptoe',
      version='1.0',
      description='Implementation of the \'Ultimate tic-tac-toe\' game.',
      author='Valentin Lorentz',
      author_email='progval@progval.net',
      url='https://github.com/ProgVal/Inceptoe',
      packages=['inceptoe', 'inceptoe.ui'],
      scripts=['inceptoe-server.py', 'inceptoe-client.py'],
     )
