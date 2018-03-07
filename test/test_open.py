import os

from .util import WithCustomCWD, WithModules, CallChecker
from kattcmd import bus as busmodule
from kattcmd.commands import init, root, open


@WithCustomCWD
@WithModules([init, root, open])
def test_OpenNewProblem(bus):
    problemname = 'carrots'
    home = os.environ['HOME']

    checker = CallChecker()
    bus.listen('kattcmd:init:directory-created', checker)
    bus.call('kattcmd:init', bus, folder=home)
    assert checker.yay

    checker = CallChecker()
    bus.listen('kattcmd:open:problem-opened', checker)
    bus.call('kattcmd:open', bus, problemname)
    assert checker.yay

    should_exist = os.path.join(home, 'kattis', problemname)
    assert os.path.exists(should_exist)


@WithCustomCWD
@WithModules([init, root, open])
def test_OpenNonExistantProblem(bus):
    # Random string, that has a very little risk of being a problem
    problemname = '784c114ff7c9865cc26f69cc05868a6e9af3a4fdd2a6b6f2331'
    home = os.environ['HOME']

    checker = CallChecker()
    bus.listen('kattcmd:init:directory-created', checker)
    bus.call('kattcmd:init', bus, folder=home)
    assert checker.yay

    checker = CallChecker()
    bus.listen('kattcmd:open:problem-doesnt-exist', checker)
    bus.call('kattcmd:open', bus, problemname)
    assert checker.yay

    should_be_empty1 = os.path.join(home, 'kattis', problemname)
    should_be_empty2 = os.path.join(home, 'test', problemname)
    assert not os.path.exists(should_be_empty1)
    assert not os.path.exists(should_be_empty2)
