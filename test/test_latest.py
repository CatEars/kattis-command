import os

from .util import WithMostModules, WithCustomCWD, ExecuteInOrder

@WithCustomCWD
@WithMostModules
def test_latest(bus):
    home = os.environ['HOME']
    problemname = 'carrots'
    problemfolder = os.path.join(home, 'kattis', problemname)
    calls = [
        ('kattcmd:init', 'kattcmd:init:directory-created'),
        ('kattcmd:open', 'kattcmd:open:problem-opened', [problemname]),
        ('kattcmd:template:python', 'kattcmd:template:python-added', [problemfolder], {'default': True})
    ]

    assert all(checker.yay for _, checker in ExecuteInOrder(bus, calls))

    result = bus.call('kattcmd:latest', bus, problemname)
    assert len(result) == 2
    type, items = result
    assert type == 'python'
    items = list(map(os.path.basename, items))
    assert items == ['carrots.py']
