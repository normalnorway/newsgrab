#!/usr/bin/env python

from distutils.core import setup

setup (
    name = 'NewsGrab',
    version = '0.1.0',
    description = 'Fetches meta-data for Norwegian news articles',
    #long_description = open ('README.md').read(),
    license = 'LICENSE.txt',
    #license = 'GPLv3',
    author = 'Normal Norway',
    author_email = 'post@normal.no',
    url = 'https://github.com/normalnorway/newsgrab',

    install_requires = ['lxml'],

    packages     = ['newsgrab', 'newsgrab.parsers'],
    scripts      = ['bin/newsgrab-cli'],
)
