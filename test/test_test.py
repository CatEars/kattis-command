import os

from .util import WithMostModules, WithCustomCWD, ExecuteInOrder


@WithCustomCWD
@WithMostModules
def test_GetTestFiles(bus):
    problemname = 'carrots'
    calls = [
        ('kattcmd:init', 'kattcmd:init:directory-created'),
        ('kattcmd:open', 'kattcmd:open:problem-opened', [problemname]),
        ('kattcmd:testdownload', 'kattcmd:testdownload:downloaded', [problemname]),
        ('kattcmd:test', 'kattcmd:test:found-tests', [problemname])
    ]

    done = list(ExecuteInOrder(bus, calls))
    res = done[-1][0]
    assert all(checker.yay for _, checker in done)
    assert all(os.path.exists(input) and os.path.exists(answer) for (input, answer) in res)

