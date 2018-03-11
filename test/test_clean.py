import os

from .util import WithCustomCWD, WithMostModules, ExecuteInOrder

@WithCustomCWD
@WithMostModules
def test_Clean(bus):
    problemname = 'carrots'
    calls = [
        ('kattcmd:init', 'kattcmd:init:directory-created'),
        ('kattcmd:open', 'kattcmd:open:problem-opened', [problemname]),
        ('kattcmd:compile:python', 'kattcmd:compile:python-compiled', [problemname]),
        ('kattcmd:clean', 'kattcmd:clean:completed')
    ]

    assert all(checker.yay for _, checker in ExecuteInOrder(bus, calls))
