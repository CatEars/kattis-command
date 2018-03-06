import os

from .util import WithCustomHome, WithModules, CallChecker
from kattcmd import core
from kattcmd import bus as busmodule
from kattcmd.commands import init, root


@WithCustomHome
@WithModules([init, root])
def test_FindRoot(bus):
    checker = CallChecker()
    home = os.environ['HOME']
    bus.listen('kattcmd:init:directory-created', checker)
    bus.call('kattcmd:init', bus, home)
    assert checker.yay

    old_dir = os.getcwd()
    os.chdir(home)
    result = bus.call('kattcmd:find-root', bus)
    assert result == home

    kattis_folder = os.path.join(home, 'kattis')
    result = bus.call('kattcmd:find-root', bus)
    assert result == home

    os.chdir(old_dir)
