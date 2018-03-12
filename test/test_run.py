import os
import tempfile

from .util import WithMostModules, WithCustomCWD, ExecuteInOrder, CallChecker


_CarrotsSolutionPy = """
import sys
a, b = map(int, sys.stdin.readline().split())
print(b)
"""

_CarrotsSolutionCpp = """
#include <iostream>
using namespace std;
int main() {
   int a;
   cin >> a >> a;
   cout << a << endl;
   return 0;
}
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
    outputs = bus.call('kattcmd:run:python', bus, [inputfname], problemname)
    assert checker.yay

    assert len(outputs) == 1
    output = outputs[0]
    assert isinstance(output, str)
    assert output.strip() == "1"


@WithCustomCWD
@WithMostModules
def test_CppRun(bus):
    problemname = 'carrots'
    calls = [
        ('kattcmd:init', 'kattcmd:init:directory-created'),
        ('kattcmd:open', 'kattcmd:open:problem-opened', [problemname])
    ]
    assert all(checker.yay for _, checker in ExecuteInOrder(bus, calls))

    home = os.environ['HOME']
    source_path = os.path.join(home, 'kattis', problemname, problemname + '.cpp')
    with open(source_path, 'w') as f:
        f.write(_CarrotsSolutionCpp)

    calls = [
        ('kattcmd:compile:cpp', 'kattcmd:compile:cpp-compiled', [problemname])
    ]
    assert all(checker.yay for _, checker in ExecuteInOrder(bus, calls))

    home = os.environ['HOME']

    inputfname = os.path.join(home, 'test1.in')
    with open(inputfname, 'w') as f:
        f.write("2 1")

    checker = CallChecker()
    bus.listen('kattcmd:run:executed', checker)
    outputs = bus.call('kattcmd:run:cpp', bus, [inputfname], problemname)
    assert checker.yay

    assert len(outputs) == 1
    output = outputs[0]
    assert isinstance(output, str)
    assert output.strip() == "1"
