import os

from .util import WithCustomCWD, WithModules, CallChecker
from kattcmd import bus as busmodule
from kattcmd.commands import init, root, test_download


@WithCustomCWD
@WithModules([init, root, test_download])
def test_DownloadWithExisting(bus):
    problem_to_download = 'carrots'
    home = os.environ['HOME']
    checker = CallChecker()

    bus.listen('kattcmd:init:directory-created', checker)
    bus.call('kattcmd:init', bus, home)
    assert checker.yay

    checker = CallChecker()
    bus.listen('kattcmd:testdownload:downloaded', checker)
    bus.call('kattcmd:testdownload', bus, problem_to_download)
    assert checker.yay

    expected = os.path.join(home, 'tests', 'carrots')
    assert os.path.isdir(expected)
    assert os.listdir(expected)


@WithCustomCWD
@WithModules([init, root, test_download])
def test_DownloadWithoutExisting(bus):
    problem_to_download = 'hello'
    home = os.environ['HOME']
    checker = CallChecker()

    bus.listen('kattcmd:init:directory-created', checker)
    bus.call('kattcmd:init', bus, home)
    assert checker.yay

    checker = CallChecker()
    bus.listen('kattcmd:testdownload:bad-status', checker)
    bus.call('kattcmd:testdownload', bus, problem_to_download)
    assert checker.yay

    expected = os.path.join(home, 'tests', 'hello')
    assert os.path.isdir(expected)
    assert not os.listdir(expected)
