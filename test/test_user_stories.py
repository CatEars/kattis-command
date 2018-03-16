import os

from .util import WithCustomCWD, WithModules, CallChecker
from kattcmd import bus as busmodule
from kattcmd.commands import init, config, template, root, open as OpenCommand, test_download


def HundredPercentRandomName():
    return '73411eb880e0e70ad89ea1f3ab86586e386a83a3a1d4c5f458680629f0313ed286f5cb0e493d7ebb'


@WithCustomCWD
@WithModules([init, template, config, root, OpenCommand, test_download])
def test_OpenNewProblem(bus):
    '''This user story tests a single longer interaction with the system.

    It starts out by initiating a repository going on to setting
    different config values (such as name). Then it opens and
    downloads tests for the problem 'carrots'.

    All of the actions are checked that they completed and worked
    afterwards.

    '''

    def ExecuteRPC(topiccall, answer_topic):
        checker = CallChecker()
        bus.listen(answer_topic, checker)
        result = topiccall()
        assert checker.yay
        return result

    def FromRoot(path):
        root = bus.call('kattcmd:find-root', bus)
        return os.path.join(root, path)

    def ExistsFromRoot(path):
        return os.path.exists(FromRoot(path))

    def FileContains(fpath, pattern):
        with open(fpath, 'r') as f:
            data = f.read()
        return pattern in data

    name = HundredPercentRandomName()
    problem = 'carrots'
    home = os.environ['HOME']

    # Init the kattis directory
    do_init = lambda: bus.call('kattcmd:init', bus, folder=home)
    ExecuteRPC(do_init, 'kattcmd:init:directory-created')
    directories = ['kattis', 'templates', 'build', 'tests', 'library']
    assert all(map(ExistsFromRoot, directories))

    # Add name to config and check it
    do_config = lambda: bus.call('kattcmd:config:add-user', bus, 'name', name)
    do_load_config = lambda: bus.call('kattcmd:config:load-user', bus, 'name')
    ExecuteRPC(do_config, 'kattcmd:config:add-user-success')
    value = ExecuteRPC(do_load_config, 'kattcmd:config:load-user-success')
    assert value == name

    # Open carrots problem, download tests
    do_open = lambda: bus.call('kattcmd:open', bus, problem)
    do_download = lambda: bus.call('kattcmd:testdownload', bus, problem)

    ExecuteRPC(do_open, 'kattcmd:open:problem-opened')
    assert ExistsFromRoot('kattis/carrots')
    ExecuteRPC(do_download, 'kattcmd:testdownload:downloaded')
    assert ExistsFromRoot('tests/carrots')

    # Add a python template and replace with info
    do_template = lambda: bus.call('kattcmd:template:python', bus, FromRoot('kattis/carrots'), default=True)
    path = ExecuteRPC(do_template, 'kattcmd:template:python-added')
    assert ExistsFromRoot('kattis/carrots/carrots.py')
    do_replace = lambda: bus.call('kattcmd:template:add-info', bus, path)
    ExecuteRPC(do_replace, 'kattcmd:template:file-info-added')
    assert FileContains(path, name)


