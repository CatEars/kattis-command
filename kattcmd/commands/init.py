'''Module that supports the implementation of the kattcmd init command.'''
import os
import pydash
import click

def _FilesExist(paths, get_missing=False):
    '''Returns true if all files exist.

    if get_missing is true, returns a list of all missing files.

    '''
    def all_exist():
        return all(os.path.isfile(path) for path in paths)

    def return_missing():
        non_existing = [path for path in paths if not os.path.isfile(path)]
        return non_existing


    if not get_missing:
        return all_exist()

    return pydash.cond([
        (all_exist, pydash.constant([])),
        (pydash.stub_true, return_missing)
    ])()


def _DirectoriesExist(paths, get_missing=False):
    '''Returns true if all directories exist.

    if get_missing is true, returns a list of all missing directories.

    '''
    def all_exist():
        return all(os.path.isdir(path) for path in paths)

    def return_missing():
        non_existing = [path for path in paths if not os.path.isdir(path)]
        return non_existing


    if not get_missing:
        return all_exist()

    return pydash.cond([
        (all_exist, pydash.constant([])),
        (pydash.stub_true, return_missing)
    ])()


def InitializeKattcmdDirectory(bus, folder=None):
    '''Creates the directory structure for kattis solutions.

    If the given folder is already a kattis solution directory then
    nothing will happen.

    '''
    folder = folder or os.getcwd()
    expected_files = ['.kattcmddir']
    expected_directories = ['library', 'templates', 'kattis', 'tests', 'build']
    files = [os.path.join(folder, fname) for fname in expected_files]
    dirs = [os.path.join(folder, d) for d in expected_directories]

    def IsKattcmdAlready():
        return _FilesExist(files) and _DirectoriesExist(dirs)

    def OnDirectoryExist():
        bus.call('kattcmd:init:directory-exists', folder)


    def IsPartialDirectory():
        missing_files = _FilesExist(files, get_missing=True)
        missing_dirs = _DirectoriesExist(dirs, get_missing=True)
        current_length = len(missing_files) + len(missing_dirs)
        expected_length = len(files) + len(dirs)
        return current_length != expected_length and current_length != 0

    def OnPartialExist():
        missing_files = _FilesExist(files, get_missing=True)
        missing_dirs = _DirectoriesExist(dirs, get_missing=True)
        missing = missing_files + missing_dirs
        expected = files + dirs
        bus.call('kattcmd:init:directory-partial', folder, expected, missing)


    def DoInit():
        for dpath in dirs:
            os.mkdir(dpath)

        for fpath in files:
            with open(fpath, 'w') as f:
                pass

        bus.call('kattcmd:init:directory-created', folder)

    return pydash.cond([
        (IsKattcmdAlready, OnDirectoryExist),
        (IsPartialDirectory, OnPartialExist),
        (pydash.stub_true, DoInit)
    ])()


def Init(bus):

    def directory_exists(folder):
        '''Event for when the kattcmd directory exists.'''
        pass

    def directory_partial(folder, expected, missing):
        '''Event for when parts of a kattcmd directory exists.'''
        pass

    def directory_created(folder):
        '''Event for when a directory is created.'''
        pass

    bus.provide('kattcmd:init', InitializeKattcmdDirectory)
    bus.provide('kattcmd:init:directory-exists', directory_exists)
    bus.provide('kattcmd:init:directory-partial', directory_partial)
    bus.provide('kattcmd:init:directory-created', directory_created)


def CLI(bus, parent):

    def OnDirectoryExists(folder):
        path = os.path.relpath(folder)
        click.echo('It seems like this already is a kattcmd directory!'.format(folder))
        click.echo('Please run `kattcmd init` in an empty directory!')

    def OnDirectoryPartial(folder, expected, missing):
        click.echo('This seems to already be a kattcmd directory, but some things are missing:')
        for item in missing:
            click.echo('   - {}'.format(item))

    def OnDirectoryCreate(folder):
        click.echo('Kattcmd folder initialized.')
        bus.call('set', 'katthome', folder)

    def OnTemplatesAdded(folder):
        relative = os.path.relpath(folder)
        click.echo('Added all default templates to: {}'.format(relative))
        click.secho('Happy Coding!', bold=True)

    @click.command()
    def init():
        '''Initializes a kattis repo.

        Creates all necessary folders and files for you to maintain
        your kattis solutions and utilize kattcmd. Should (preferably)
        be done in a completely empty repo.

        The command creates 5 folders: 'library', 'templates',
        'kattis', 'tests', 'build'.

        - library: Where you keep your code library, algorithms, and
        solutions to general problems. For example you might have
        'string.hpp' or 'graph.py' in here.

        - templates: Contains templates for your code, which will be
        automatically imported to a newly opened problem, depending
        on your config.

        - kattis: Contains your solutions to different problems. Put
        all the files necessary to solve a problem inside here. For
        example the problem carrots with a single python file would
        be `kattis/carrots/carrots.py`.

        - tests: Contains your tests and the sample test cases
        downloaded from kattis. Tests are pairs where there is one
        X.in and a corresponding X.ans, for example 'carrots.01.in'
        and 'carrots.01.ans' create a test pair.

        - build: Contains binaries and scripts that are run against
        your tests. If you want to manually run something then look
        for it in here.

        '''
        bus.listen('kattcmd:init:directory-exists', OnDirectoryExists)
        bus.listen('kattcmd:init:directory-partial', OnDirectoryPartial)
        bus.listen('kattcmd:init:directory-created', OnDirectoryCreate)
        bus.call('kattcmd:init', bus)

        home = bus.call('get', 'katthome')
        if not home:
            return
        bus.listen('kattcmd:template:default-added', OnTemplatesAdded)
        bus.call('kattcmd:template:default', bus, home)

    parent.add_command(init)
