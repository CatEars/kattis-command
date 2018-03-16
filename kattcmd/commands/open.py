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

    if not os.environ.get('FORCE_OPEN', '') and not DoesProblemExist(problemname):
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

    def OnFileInfoReplaced(path):
        relative = os.path.relpath(path)
        click.echo('Updated {} with information (date etc.)'.format(relative))

    def OnTemplateAdded(folder, path):
        if not path:
            folder = os.path.relpath(folder)
            click.secho('File already exists in {}'.format(folder))
            click.secho('Did not overwrite it...')
        else:
            path = os.path.relpath(path)
            click.secho('Added {}'.format(path))
        
    @click.command()
    @click.option('--force', type=bool, default=False, is_flag=True, help='Open a problem even if it does not exist on kattis.')
    @click.argument('name')
    def open(name, force):
        '''Opens a new problem.

        Run this command when you want to start working on a solution
        to a new problem.

        Will create the folder `kattis/NAME` and put a template in
        it. Will also download any sample input/output from kattis and
        put into `tests/NAME`.

        Normally the command checks against kattis that the problem
        exists, but if you want to open one that does not exist you
        will have to use the --force flag, which will only create the
        folder and move the template there.

        '''
        bus.listen('kattcmd:open:problem-opened', OnProblemOpen)
        bus.listen('kattcmd:testdownload:downloaded', OnTestsLoaded)
        bus.listen('kattcmd:testdownload:bad-status', OnTestFail)
        bus.listen('kattcmd:open:problem-doesnt-exist', OnProblemDoesntExist)
        bus.listen('kattcmd:template:python-added', OnTemplateAdded)
        bus.listen('kattcmd:template:cpp-added', OnTemplateAdded)

        if force:
            os.environ['FORCE_OPEN'] = '1'

        bus.call('kattcmd:open', bus, name)
        bus.call('kattcmd:testdownload', bus, name)
        root = bus.call('kattcmd:find-root', bus)
        target = os.path.join(root, 'kattis', name)
        preference = bus.call('kattcmd:config:load-user', bus, 'template-type', default='python')

        if preference == 'python':
            path = bus.call('kattcmd:template:python', bus, target)
            if path:
                bus.call('kattcmd:template:add-info', bus, path)

        elif preference == 'cpp':
            path = bus.call('kattcmd:template:cpp', bus, target)
            if path:
                bus.call('kattcmd:template:add-info', bus, path)

        else:
            raise ValueError('Bad template preference, check "template-type" in your ' + \
                             'user configuration!')

    parent.add_command(open)
