import os

from .util import WithCustomCWD, WithMostModules, ExecuteInOrder


@WithCustomCWD
@WithMostModules
def test_CompilePython(bus):
    problemname = 'carrots'
    target_template = os.path.join(os.environ['HOME'], 'kattis', problemname)
    calls = [
        ('kattcmd:init', 'kattcmd:init:directory-created'),
        ('kattcmd:open', 'kattcmd:open:problem-opened', [problemname]),
        ('kattcmd:template:python', 'kattcmd:template:python-added', [target_template], {'default': True}),
        ('kattcmd:compile:python', 'kattcmd:compile:python-compiled', [problemname])
    ]

    assert all(checker.yay for _, checker in ExecuteInOrder(bus, calls))
    buildpath = os.path.join(os.environ['HOME'], 'build', problemname)
    assert 'carrots.py' in os.listdir(buildpath)


@WithCustomCWD
@WithMostModules
def test_CompileCpp(bus):
    problemname = 'carrots'
    target_template = os.path.join(os.environ['HOME'], 'kattis', problemname)
    calls = [
        ('kattcmd:init', 'kattcmd:init:directory-created'),
        ('kattcmd:open', 'kattcmd:open:problem-opened', [problemname]),
        ('kattcmd:template:cpp', 'kattcmd:template:cpp-added', [target_template], {'default': True}),
        ('kattcmd:compile:cpp', 'kattcmd:compile:cpp-compiled', [problemname])
    ]

    assert all(checker.yay for _, checker in ExecuteInOrder(bus, calls))
    buildpath = os.path.join(os.environ['HOME'], 'build', problemname)
    assert 'carrots' in os.listdir(buildpath)

