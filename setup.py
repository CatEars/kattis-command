#!/usr/bin/env python

from distutils.core import setup

setup(
    name='kattcmd',
    packages=['kattcmd', 'kattcmd.commands'],
    version='0.0.1',
    description='Kattis solution management CLI written in python',
    author='Henrik Adolfsson',
    author_email='anting004@gmail.com',
    url='https://git.lysator.liu.se/catears/kattis-command',
    download_url='httsp://git.lysator.liu.se/catears/kattis-command/master/archive.tar.gz',
    keywords=['kattis', 'cli', 'competitive programming'],
    scripts=['bin/kattcmd'],
    classifiers=[]
)
