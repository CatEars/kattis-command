import os
import configparser

from kattcmd import core
from .util import WithCustomHome



@WithCustomHome
def test_creates_kattcmd_options():
    assert core.TouchStructure()

    kattcmd_path = os.path.expanduser('~/.kattcmd')
    assert os.path.isfile(kattcmd_path)

    config = configparser.ConfigParser()
    config.read(kattcmd_path)

    assert 'options' in config
    assert 'kattisrc' in config['options']
    assert 'plugins' in config['options']


@WithCustomHome
def test_touch_twice():
    assert core.TouchStructure()
    assert not core.TouchStructure()


@WithCustomHome
def test_lists_plugins():
    assert core.TouchStructure()
    plugins = core.ListPlugins()
    assert isinstance(plugins, list)

