import os

from .util import WithCustomCWD, WithModules, CallChecker, ExecuteRPC, RunWithChecker
from kattcmd import bus as busmodule
from kattcmd.commands import init, template, open as open_command, root, compile as compile_command

def InitAndOpenProblem(bus, problemname):
    assert RunWithChecker(bus, 'kattcmd:init', 'kattcmd:init:directory-created', bus).yay
    assert RunWithChecker(bus, 'kattcmd:open', 'kattcmd:open:problem-opened', bus, problemname).yay


@WithCustomCWD
@WithModules([init, root, open_command, template, compile_command])
def test_CompilePython(bus):
    problemname = 'carrots'
    InitAndOpenProblem(bus, problemname)

    problemfolder = os.path.join(os.environ['HOME'], 'kattis', problemname)
    topic = 'kattcmd:template:python'
    answertopic = 'kattcmd:template:python-added'
    assert RunWithChecker(bus, topic, answertopic, bus, problemfolder).yay

    topic = 'kattcmd:compile:python'
    answertopic = 'kattcmd:compile:python-compiled'
    result, checker = ExecuteRPC(bus, topic, answertopic, bus, problemname)
    assert checker.yay

    buildpath = os.path.join(os.environ['HOME'], 'build', problemname)
    outputfiles = [os.path.basename(fpath) for fpath in result]
    assert set(os.listdir(buildpath)) == set(outputfiles)


@WithCustomCWD
@WithModules([init, root, open_command, template, compile_command])
def test_CompileCpp(bus):
    pass
