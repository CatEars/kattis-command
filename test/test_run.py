import os
import tempfile

from .util import WithMostModules, WithCustomCWD, ExecuteInOrder, CallChecker


_CarrotsSolutionPy = """
import sys
a, b = map(int, sys.stdin.readline().split())
print(b)
"""

@WithCustomCWD
@WithMostModules
def test_PythonRun(bus):
    problemname = 'carrots'
    calls = [
        ('kattcmd:init', 'kattcmd:init:directory-created'),
        ('kattcmd:open', 'kattcmd:open:problem-opened', [problemname]),
        ('kattcmd:compile:python', 'kattcmd:compile:python-compiled', [problemname])
    ]

    assert all(checker.yay for _, checker in ExecuteInOrder(bus, calls))

    home = os.environ['HOME']

    runner = os.path.join(home, 'build', problemname, problemname + '.py')
    with open(runner, 'w') as f:
        f.write(_CarrotsSolutionPy)

    inputfname = os.path.join(home, 'test1.in')
    with open(inputfname, 'w') as f:
        f.write("2 1")

    checker = CallChecker()
    bus.listen('kattcmd:run:executed', checker)
    processes = bus.call('kattcmd:run:python', bus, [inputfname], problemname)
    assert checker.yay

    assert len(processes) == 1
    process = processes[0]
    assert process.returncode == 0
    assert process.stdout.strip() == "1"

