import os
import click
import difflib


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


def CLI(bus, parent):


    def PrintDiffHelp():
        click.secho('')

    @parent.command()
    @click.argument('name')
    def test(name):
        # Compile name under most appropriate language
        root = bus.call('kattcmd:find-root', bus)

        if not name in os.listdir(os.path.join(root, 'kattis')):
            click.secho('Could not find problem with name: {}'.format(name), fg='red')
            return

        cpp_endings = ['.cpp', '.cxx', '.cc']
        directory = os.path.join(root, 'kattis', name)
        items = os.listdir(directory)
        if '{}.py'.format(name) in items:
            files = bus.call('kattcmd:compile:python', bus, name)
            topic = 'kattcmd:run:python'
            args = [name]

        elif any('{}{}'.format(name, ext) in items for ext in cpp_endings):
            binary = bus.call('kattcmd:compile:cpp', bus, name)
            binary = os.path.relpath(binary)
            click.secho('Not implemented yet, but binary is compiled and at {}'.format(binary))
            return

        else:
            click.secho('Could not find main program to be either C++ or Python')
            return
        items = [os.path.join(directory, item) for item in items]

        # Find all test files
        tests = list(sorted(bus.call('kattcmd:test', bus, name)))
        inputs = [input for input, _ in tests]
        answers = [answer for _, answer in tests]

        # Run against all text files
        outputs = bus.call(topic, bus, inputs, *args)

        first = True
        # Output the diffs between the text files
        for idx, (input, answer, output) in enumerate(zip(inputs, answers, outputs)):
            input, answer = map(os.path.relpath, [input, answer])
            to_print = []

            if not isinstance(output, str):
                # Is probably an error
                to_print = [str(output)]
                any_diff = True
            else:
                with open(answer, 'r') as f:
                    data = [x.strip() for x in f.readlines()]
                output = [x.strip() for x in output.strip().split('\n')]

                def IsJunk(line):
                    return not line.strip()
                diff = difflib.ndiff(data, output, linejunk=IsJunk)

                any_diff = False
                for line in diff:
                    wrong = ['? ', '- ', '+ ']
                    if any(line.startswith(x) for x in wrong):
                        any_diff = True
                        to_print.append(line)

            if not first:
                click.secho('')
            first = False
            click.secho('{}: {}'.format(idx, input), bold=True)

            if to_print:
                msg = '=== Diff start ==='
                click.secho(msg, bold=True)
                for line in to_print:
                    click.echo(line)

                click.secho('=== Stop ===', bold=True)
                click.secho('   Nope', fg='red')

            elif not to_print and not any_diff:
                click.secho('   OK', fg='green')

            else:
                msg = '{}: {} as input not OK, but nothing to output (?)'
                click.secho(msg.format(idx, input), fg='red')
