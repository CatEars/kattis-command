import os

from kattcmd import core
from kattcmd import bus as busmodule
from kattcmd.commands import init
from .util import WithCustomHome, WithModules, CallChecker



@WithCustomHome
@WithModules([init])
def test_initialize(bus):
    checkers = [CallChecker(), CallChecker(), CallChecker()]

    bus.listen('kattcmd:init:directory-created', checkers[0])
    bus.listen('kattcmd:init:directory-exists', checkers[1])
    bus.listen('kattcmd:init:directory-partial', checkers[2])

    home = os.environ['HOME']

    bus.call('kattcmd:init', bus, folder=home)
    assert checkers[0].yay
    assert checkers[1].nay
    assert checkers[2].nay

    expected_directories = ['templates', 'kattis', 'tests', 'build', 'library']
    D = set(os.path.join(home, d) for d in expected_directories)
    U = set(os.path.join(home, fname) for fname in os.listdir(home))
    assert D.issubset(U)

    bus.call('kattcmd:init', bus, folder=home)
    assert checkers[1].yay
    assert checkers[2].nay

    os.rmdir(os.path.join(home, 'kattis'))
    bus.call('kattcmd:init', bus, folder=home)
    assert checkers[2].yay
