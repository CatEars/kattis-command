import os
import click


def OpenProblem(bus, problemname):
    '''Opens the problem inside the kattis folder.'''
    root = bus.call('kattcmd:find-root', bus)
    problem_path = os.path.join(root, 'kattis', problemname)
    if not os.path.isdir(problem_path):
        os.mkdir(problem_path)
        bus.call('kattcmd:open:problem-opened', problem_path)
    else:
        bus.call('kattcmd:open:problem-already-opened', problem_path)


def Init(bus):
    def on_problem_opened(path):
        '''Event called when a problem is opened.'''

    def on_problem_already_opened(path):
        '''Event called when the problem already exists.'''

    bus.provide('kattcmd:open', OpenProblem)
    bus.provide('kattcmd:open:problem-opened', on_problem_opened)
    bus.provide('kattcmd:open:problem-already-opened', on_problem_already_opened)


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

    @click.command()
    @click.argument('name')
    def open(name):
        bus.listen('kattcmd:open:problem-opened', OnProblemOpen)
        bus.listen('kattcmd:testdownload:downloaded', OnTestsLoaded)
        bus.listen('kattcmd:testdownload:bad-status', OnTestFail)

        bus.call('kattcmd:open', bus, name)
        bus.call('kattcmd:testdownload', bus, name)

    parent.add_command(open)
