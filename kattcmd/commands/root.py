from pathlib import Path
import os
import configparser


class FindRootException(Exception):

    def __init__(self, message):
        self.message = message


def _IsKattisDirectory(path):
    return (path / '.kattcmddir').exists() or (
        (path / 'templates').exists() and
        (path / 'library').exists() and
        (path / 'kattis').exists() and
        (path / 'tests').exists() and
        (path / 'build').exists()
    )


def FindKattisRoot(bus):
    '''Finds the root of the kattis directory from the current working directory.'''
    now = Path(os.getcwd())
    paths_to_check = [now] + [parent for parent in now.parents]
    for directory in filter(_IsKattisDirectory, paths_to_check):
        return str(directory)

    # Check if there exists a default directory, else none exists
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/.kattcmd'))

    if 'options' in config and 'default-kattis' in config['options'] and \
       config['options']['default-kattis']:
        return config['options']['default-kattis']

    raise FindRootException('Could not find a kattis directory when searching from {}'.format(now))


def Init(bus):
    bus.provide('kattcmd:find-root', FindKattisRoot)
