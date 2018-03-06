import os

from .util import WithCustomCWD, WithModules, CallChecker
from kattcmd import bus as busmodule
from kattcmd.commands import init, root


@WithCustomCWD
@WithModules([init, root])
def test_FindRoot(bus):
    checker = CallChecker()
    home = os.environ['HOME']
    bus.listen('kattcmd:init:directory-created', checker)
    bus.call('kattcmd:init', bus, home)
    assert checker.yay

    result = bus.call('kattcmd:find-root', bus)
    assert result == home

    kattis_folder = os.path.join(home, 'kattis')
    result = bus.call('kattcmd:find-root', bus)
    assert result == home
