import os
import pytest
import configparser

from .util import WithMostModules, WithCustomCWD, ExecuteInOrder

_CarrotsSolution = """
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

def ShouldSkipSubmit():
    expected_envs = [
        'KATTIS_TOKEN',
        'KATTIS_USER',
        'KATTIS_LOGIN',
        'KATTIS_SUBMISSION'
    ]
    return not all(map(os.getenv, expected_envs))


def SetupKattisRC():

    home = os.environ['HOME']
    fpath = os.path.join(home, '.kattisrc')

    envs = [
        'KATTIS_USER',
        'KATTIS_TOKEN',
        'KATTIS_LOGIN',
        'KATTIS_SUBMISSION'
    ]
    user, token, login, submit = map(os.getenv, envs)

    config = configparser.ConfigParser()
    config['user'] = {
        'username': user,
        'token': token
    }
    config['kattis'] = {
        'loginurl': login,
        'submissionurl': submit
    }

    with open(fpath, 'w') as f:
        config.write(f)


@pytest.mark.submission
@pytest.mark.skipif(ShouldSkipSubmit(), reason='No environment variables for running submit')
@WithCustomCWD
@WithMostModules
def test_SubmitCarrotsWithPython(bus):
    SetupKattisRC()
    problemname = 'carrots'
    solution = _CarrotsSolution

    # Init and open carrots problem
    calls = [
        ('kattcmd:init', 'kattcmd:init:directory-created'),
        ('kattcmd:open', 'kattcmd:open:problem-opened', [problemname])
    ]
    assert all(checker.yay for _, checker in ExecuteInOrder(bus, calls))

    # Create solution
    home = bus.call('kattcmd:find-root', bus)
    target = os.path.join(home, 'kattis', problemname, problemname + '.py')
    with open(target, 'w') as f:
        f.write(solution)

    # Submit
    calls = [
        ('kattcmd:submit:python', 'kattcmd:submit:submitted', [problemname])
    ]

    results = list(ExecuteInOrder(bus, calls))
    assert len(results) == 1

    # Check call and that the text received from kattis is as expected
    result, checker = results[0]
    assert checker.yay
    assert result.text and isinstance(result.text, str)
    assert 'Submission ID:' in result.text


@pytest.mark.submission
@pytest.mark.skipif(ShouldSkipSubmit(), reason='No environment variables for running submit')
@WithCustomCWD
@WithMostModules
def test_SubmitCarrotsWithCpp(bus):
    SetupKattisRC()
    problemname = 'carrots'
    solution = _CarrotsSolutionCpp

    # Init and open carrots problem
    calls = [
        ('kattcmd:init', 'kattcmd:init:directory-created'),
        ('kattcmd:open', 'kattcmd:open:problem-opened', [problemname])
    ]
    assert all(checker.yay for _, checker in ExecuteInOrder(bus, calls))

    # Create solution
    home = bus.call('kattcmd:find-root', bus)
    target = os.path.join(home, 'kattis', problemname, problemname + '.cpp')
    with open(target, 'w') as f:
        f.write(solution)

    # Submit
    calls = [
        ('kattcmd:submit:cpp', 'kattcmd:submit:submitted', [problemname])
    ]

    results = list(ExecuteInOrder(bus, calls))
    assert len(results) == 1

    # Check call and that the text received from kattis is as expected
    result, checker = results[0]
    assert checker.yay
    assert result.text and isinstance(result.text, str)
    assert 'Submission ID:' in result.text

