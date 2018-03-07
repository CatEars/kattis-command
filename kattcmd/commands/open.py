import os
import click
import requests


def DoesProblemExist(problemname):
    '''Checks against kattis that a problem exists.'''
    url = 'https://open.kattis.com/problems/{}'.format(problemname)
    response = requests.get(url)
    return response.status_code == 200


def OpenProblem(bus, problemname):
    '''Opens the problem inside the kattis folder.'''
    root = bus.call('kattcmd:find-root', bus)
    problem_path = os.path.join(root, 'kattis', problemname)

    if not DoesProblemExist(problemname):
        bus.call('kattcmd:open:problem-doesnt-exist', problemname)

    elif os.path.isdir(problem_path):
        bus.call('kattcmd:open:problem-already-opened', problem_path)

    else:
        os.mkdir(problem_path)
        bus.call('kattcmd:open:problem-opened', problem_path)


def Init(bus):

    def OnProblemOpened(path):
        '''Event called when a problem is opened.'''

    def OnProblemAlreadyOpened(path):
        '''Event called when the problem already exists.'''

    def OnProblemDoesntExist(problem):
        '''Event called when a problem does not exist'''

    bus.provide('kattcmd:open', OpenProblem)
    bus.provide('kattcmd:open:problem-opened', OnProblemOpened)
    bus.provide('kattcmd:open:problem-already-opened', OnProblemAlreadyOpened)
    bus.provide('kattcmd:open:problem-doesnt-exist', OnProblemDoesntExist)


def CLI(bus, parent):

    def OnProblemOpen(path):
        name = os.path.basename(path)
        click.echo('Opened {} for solving'.format(name))

    def OnProblemAlreadyOpened(path):
        name = os.path.basename(path)
        click.echo('{} is already opened, it seems like'.format(name))

    def OnTestsLoaded(testdir):
        relative = os.path.relpath(testdir)
        click.echo('Tests put inside of {}'.format(relative))

    def OnTestFail(response):
        click.echo('Could not automatically download tests.')

    def OnProblemDoesntExist(problem):
        click.echo('Could not find problem {}'.format(problem))
        exit(0)

    @click.command()
    @click.argument('name')
    def open(name):
        bus.listen('kattcmd:open:problem-opened', OnProblemOpen)
        bus.listen('kattcmd:testdownload:downloaded', OnTestsLoaded)
        bus.listen('kattcmd:testdownload:bad-status', OnTestFail)
        bus.listen('kattcmd:open:problem-doesnt-exist', OnProblemDoesntExist)

        bus.call('kattcmd:open', bus, name)
        bus.call('kattcmd:testdownload', bus, name)

    parent.add_command(open)
