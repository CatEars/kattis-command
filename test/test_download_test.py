import os

from .util import WithCustomCWD, WithMostModules, ExecuteInOrder

@WithCustomCWD
@WithMostModules
def test_DownloadWithExisting(bus):
    problemname = 'carrots'
    home = os.environ['HOME']
    calls = [
        ('kattcmd:init', 'kattcmd:init:directory-created'),
        ('kattcmd:testdownload', 'kattcmd:testdownload:downloaded', [problemname])
    ]
    assert all(checker.yay for _, checker in ExecuteInOrder(bus, calls))

    expected = os.path.join(home, 'tests', 'carrots')
    assert os.path.isdir(expected)
    assert os.listdir(expected)


@WithCustomCWD
@WithMostModules
def test_DownloadWithoutExisting(bus):
    problemname = 'hello' # Has no sample input
    home = os.environ['HOME']
    calls = [
        ('kattcmd:init', 'kattcmd:init:directory-created'),
        ('kattcmd:testdownload', 'kattcmd:testdownload:bad-status', [problemname])
    ]
    assert all(checker.yay for _, checker in ExecuteInOrder(bus, calls))

    expected = os.path.join(home, 'tests', 'hello')
    assert os.path.isdir(expected)
    assert not os.listdir(expected)
