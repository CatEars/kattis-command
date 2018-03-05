import os
import tempfile
import configparser

from kattcmd import core


def with_custom_home(f):
    '''Descriptor for tests that should run in their own isolated environment.'''
    def inner(*args, **kwargs):
        with tempfile.TemporaryDirectory() as tempdirname:
            os.environ['HOME'] = tempdirname
            f(*args, **kwargs)

    return inner


@with_custom_home
def test_creates_kattcmd_options():
    assert core.TouchStructure()

    kattcmd_path = os.path.expanduser('~/.kattcmd')
    assert os.path.isfile(kattcmd_path)

    config = configparser.ConfigParser()
    config.read(kattcmd_path)

    assert 'options' in config
    assert 'kattisrc' in config['options']
    assert 'plugins' in config['options']


@with_custom_home
def test_touch_twice():
    assert core.TouchStructure()
    assert not core.TouchStructure()


@with_custom_home
def test_lists_plugins():
    assert core.TouchStructure()
    plugins = core.ListPlugins()
    assert isinstance(plugins, list)

