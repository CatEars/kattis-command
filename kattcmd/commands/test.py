import os


def _GetTestFolder(root, problemname):
    '''Returns the test folder for a problem.'''
    return os.path.join(root, 'tests', problemname)


def _GetTestFilesForProblem(root, problemname):
    '''Returns the files in a problem folder.'''
    items = os.listdir(_GetTestFolder(root, problemname))
    return [os.path.join(_GetTestFolder(root, problemname), item) for item in items]


def GetTestsForProblem(bus, name):
    '''Returns the tests for a given problem.'''
    home = bus.call('kattcmd:find-root', bus)
    tests = _GetTestFilesForProblem(home, name)

    if not tests:
        bus.call('kattcmd:test:no-tests', name)
        return

    def PathWithoutExt(fpath):
        return os.path.splitext(fpath)[0]

    ins = [PathWithoutExt(fpath) for fpath in tests if fpath.endswith('.in')]
    ans = [PathWithoutExt(fpath) for fpath in tests if fpath.endswith('.ans')]

    inputs = set(ins)
    answers = set(ans)
    both_input_and_answer = inputs & answers

    values = [(test + '.in', test + '.ans') for test in both_input_and_answer]
    bus.call('kattcmd:test:found-tests', name, values)
    return values


def Init(bus):

    def OnNoTests(problemname):
        '''Called when problem has no tests available.'''

    def OnTestsFound(problemname, tests):
        '''Called when tests have been found for a particular problem.'''


    bus.provide('kattcmd:test', GetTestsForProblem)
    bus.provide('kattcmd:test:no-tests', OnNoTests)
    bus.provide('kattcmd:test:found-tests', OnTestsFound)
