import os

from kattcmd import core
from kattcmd import bus as busmodule
from kattcmd.commands import init
from .util import with_custom_home, CallChecker



@with_custom_home
def test_initialize():
    assert core.TouchStructure()

    checkers = [CallChecker(), CallChecker(), CallChecker()]

    bus = busmodule.Bus()
    bus.listen('kattcmd:init:directory-created', checkers[0])
    bus.listen('kattcmd:init:directory-exists', checkers[1])
    bus.listen('kattcmd:init:directory-partial', checkers[2])
    init.Init(bus)

    bus.call('kattcmd:init', bus, folder=os.environ['HOME'])
    assert checkers[0].yay
    assert checkers[1].nay
    assert checkers[2].nay

    bus.call('kattcmd:init', bus, folder=os.environ['HOME'])
    assert checkers[1].yay
    assert checkers[2].nay

    os.rmdir(os.path.join(os.environ['HOME'], 'kattis'))
    bus.call('kattcmd:init', bus, folder=os.environ['HOME'])
    assert checkers[2].yay
