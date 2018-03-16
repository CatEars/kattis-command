import os

from .util import WithCustomCWD, WithMostModules, ExecuteInOrder


@WithCustomCWD
@WithMostModules
def test_OpenNewProblem(bus):
    problemname = 'carrots'
    home = os.environ['HOME']
    calls = [
        ('kattcmd:init', 'kattcmd:init:directory-created'),
        ('kattcmd:open', 'kattcmd:open:problem-opened', [problemname])
    ]
    assert all(checker.yay for _, checker in ExecuteInOrder(bus, calls))

    should_exist = os.path.join(home, 'kattis', problemname)
    assert os.path.exists(should_exist)


@WithCustomCWD
@WithMostModules
def test_OpenNonExistantProblem(bus):
    # Random string, that has a very little risk of being a problem
    problemname = '784c114ff7c9865cc26f69cc05868a6e9af3a4fdd2a6b6f2331'
    home = os.environ['HOME']
    calls = [
        ('kattcmd:init', 'kattcmd:init:directory-created'),
        ('kattcmd:open', 'kattcmd:open:problem-doesnt-exist', [problemname])
    ]
    assert all(checker.yay for _, checker in ExecuteInOrder(bus, calls))

    should_be_empty1 = os.path.join(home, 'kattis', problemname)
    should_be_empty2 = os.path.join(home, 'test', problemname)
    assert not os.path.exists(should_be_empty1)
    assert not os.path.exists(should_be_empty2)
