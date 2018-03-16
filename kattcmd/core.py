import ast
import os
import configparser
import importlib

from kattcmd import commands


class CredentialsException(Exception):
    '''An exception type for missing credentials.'''


def ImportExternal(path):
    '''Checks that path is a plugin.'''
    name, extension = os.path.splitext(path)
    if extension != '.py':
        return ('extension', (path, extension))
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return ('success', module)
    except ImportError as e:
        return ('error', (path, e))
    except OSError as e:
        return ('error', (path, e))


def TouchStructure():
    '''Initializes the .kattcmd file in the users home directory.'''
    # Create ~/.kattcmd and store:
    # - Path to .kattisrc file
    # - Empty list of plugins

    # [options]
    # kattisrc=~/.kattisrc (check that it exists)
    # plugins=[]

    user_folder = os.path.expanduser('~')
    kattcmd_file = os.path.join(user_folder, '.kattcmd')
    if not os.path.isfile(kattcmd_file):
        config = configparser.ConfigParser()
        config['options'] = {
            'kattisrc': os.path.expanduser('~/.kattisrc'),
            'plugins': []
        }

        with open(kattcmd_file, 'w') as configfile:
            config.write(configfile)

        return True
    return False


def _ListBuiltins():
    '''Returns a list of all the builtin plugins.'''
    return [commands.init, commands.template, commands.open, commands.root,
            commands.test_download, commands.config, commands.compile,
            commands.test, commands.run, commands.submit, commands.clean,
            commands.tips, commands.latest, commands.plugin]


def _ListExternals():
    '''Returns a list of all user-added plugins.'''
    config_path = os.path.expanduser('~/.kattcmd')
    config = configparser.ConfigParser()
    config.read(config_path)

    # See https://stackoverflow.com/questions/1894269/convert-string-representation-of-list-to-list-in-python
    # for why we use ast.literal_eval here
    L = ast.literal_eval(config['options']['plugins'])
    return [x.strip() for x in L if x.strip()]


def ListPlugins():
    '''Returns a list of all plugins, which is all available commands used by the program.'''
    return _ListBuiltins() + _ListExternals()
