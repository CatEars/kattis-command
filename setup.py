#!/usr/bin/env python

# How to update:
# 0. source the virtualenv
# 1. Create a new tag on gitlab and find the download url (archive.tar.gz) for that tag
# 2. Update the version in setup()
# 3. run `python setup.py sdist` and test with tar.gz in dist folder
# 4. run `twine upload dist/YOUR_NEWLY_CREATED_ARCHIVE.tar.gz`

from distutils.core import setup

setup(
    name='kattcmd',
    packages=['kattcmd', 'kattcmd.commands'],
    version='0.0.7',
    description='Kattis solution management CLI written in python',
    author='Henrik Adolfsson',
    author_email='anting004@gmail.com',
    url='https://git.lysator.liu.se/catears/kattis-command',
    download_url='https://git.lysator.liu.se/catears/kattis-command/repository/0.0.7/archive.tar.gz',
    keywords=['kattis', 'cli', 'competitive programming'],
    install_requires=['requests', 'click', 'pydash'],
    python_requires='>=3.4',
    scripts=['bin/kattcmd'],
    package_dir={
        'kattcmd.commands': 'kattcmd/commands'
    },
    package_data={
        'kattcmd.commands': ['default_templates/*']
    },
    classifiers=[]
)
