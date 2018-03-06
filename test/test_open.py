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
