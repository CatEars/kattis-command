import os
import configparser


class CredentialsException(Exception):
    '''An exception type for missing credentials.'''


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
            configfile.write(config)

        return True
    return False


def _ListBuiltins():
    '''Returns a list of all the builtin plugins.'''
    return []


def _ListExternals():
    '''Returns a list of all user-added plugins.'''
    config_path = os.path.expanduser('~/.kattcmd')
    config = configparser.ConfigParser()
    config.read(config_path)
    return config['options']['plugins']


def ListPlugins():
    '''Returns a list of all plugins, which is all available commands used by the program.'''
    return _ListBuiltins() + _ListExternals()
