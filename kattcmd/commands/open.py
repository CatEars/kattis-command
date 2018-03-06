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

    @click.command()
    @click.argument('name')
    def open(name):
        bus.call('kattcmd:open', bus, name)
        bus.call('kattcmd:testdownload', bus, name)

    parent.add_command(open)

