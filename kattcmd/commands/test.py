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

    def OnNoTestsFound(name):
        click.secho('No tests found for {}'.format(name), fg='red')
        click.secho('Exiting')
        exit(1)

    def OnPythonCompiled(paths):
        basenames = list(map(os.path.basename, paths))
        click.secho('Python files moved to build folder [{}]'.format(', '.join(basenames)))

    def OnCppCompiled(binary):
        click.secho('Cpp compiled successfully and put in {}'.format(binary))

    def OnCppFailed(compile_command, directory):
        directory = os.path.relpath(directory)
        click.secho('Could not compile using: "{}" in {}'.format(compile_command, directory), fg='red')
        click.secho('Exiting')
        exit(1)

    def OnNoExecutable(name, type):
        click.secho('Could not manage to find an executable for {}. Was looking for a {} file'.format(name, type), fg='red')
        exit(1)

    def OnNoFiles(problemname):
        click.secho('Could not find any files for problem "{}"'.format(problemname), fg='red')
        click.echo('Exiting')
        exit(1)

    @parent.command()
    @click.argument('name')
    def test(name):
        '''Test your solution to a problem.

        Once you have implemented a solution to a problem you can
        automatically test it using this command. It will run against
        all the different tests that are defined for the problem in
        the tests folder and output a diff between your program output
        and the answers.

        When running the program it will use a timeout of ten seconds.

        '''
        bus.listen('kattcmd:test:no-tests', OnNoTestsFound)
        bus.listen('kattcmd:compile:python-compiled', OnPythonCompiled)
        bus.listen('kattcmd:compile:cpp-compiled', OnCppCompiled)
        bus.listen('kattcmd:compile:cpp-compile-failed', OnCppFailed)
        bus.listen('kattcmd:run:no-executable', OnNoExecutable)
        bus.listen('kattcmd:latest:no-files', OnNoFiles)

        # Compile name under most appropriate language
        root = bus.call('kattcmd:find-root', bus)

        if not name in os.listdir(os.path.join(root, 'kattis')):
            click.secho('Could not find problem with name: {}'.format(name), fg='red')
            return

        # TODO: below should use kattcmd:latest
        language, items = bus.call('kattcmd:latest', bus, name)
        topic_mapping = {
            'python': ('kattcmd:compile:python', 'kattcmd:run:python'),
            'cpp': ('kattcmd:compile:cpp', 'kattcmd:run:cpp')
        }

        if not language in topic_mapping:
            click.secho('Cannot run for language: {}'.format(language), fg='red')
            return

        compile_topic, run_topic = topic_mapping[language]
        args = [name]

        # Find all test files
        tests = list(sorted(bus.call('kattcmd:test', bus, name)))
        inputs = [input for input, _ in tests]
        answers = [answer for _, answer in tests]

        # Run against all text files
        compiled = bus.call(compile_topic, bus, *args)
        if not compiled:
            return
        outputs = bus.call(run_topic, bus, inputs, *args)

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
