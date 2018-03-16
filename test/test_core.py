import os
import configparser

from kattcmd import core
from .util import WithCustomHome



@WithCustomHome
def test_CreatesKattcmdOptions():
    assert core.TouchStructure()

    kattcmd_path = os.path.expanduser('~/.kattcmd')
    assert os.path.isfile(kattcmd_path)

    config = configparser.ConfigParser()
    config.read(kattcmd_path)

    assert 'options' in config
    assert 'kattisrc' in config['options']
    assert 'plugins' in config['options']


@WithCustomHome
def test_TouchTwice():
    assert core.TouchStructure()
    assert not core.TouchStructure()


@WithCustomHome
def test_ListsPlugins():
    assert core.TouchStructure()
    plugins = core.ListPlugins()
    assert isinstance(plugins, list)

