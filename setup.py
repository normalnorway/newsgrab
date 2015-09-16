#!/usr/bin/env python

from distutils.core import setup
#from setuptools import setup

# UserWarning: Normalizing '0.1.dev' to '0.1.dev0' normalized_version,

setup (
    name = 'NewsGrab',
    version = '0.1.dev',
    description = 'Fetches meta-data for Norwegian news articles',
    #long_description = open ('README.md').read(),
    license = 'LICENSE.txt',
    #license = 'GPLv3',
    author = 'Normal Norway',
    author_email = 'post@normal.no',
    url = 'https://github.com/normalnorway/newsgrab',

    # UserWarning: Unknown distribution option: 'install_requires'
    #install_requires = ['lxml'],

    packages     = ['newsgrab', 'newsgrab.parsers'],
)
