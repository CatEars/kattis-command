'''Module that supports the implementation of the kattcmd init command.'''
import os
import pydash


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
    expected_directories = ['library', 'templates', 'kattis']
    files = [os.path.join(folder, fname) for fname in expected_files]
    dirs = [os.path.join(folder, d) for d in expected_directories]

    def is_kattcmd_already():
        return _FilesExist(files) and _DirectoriesExist(dirs)

    def on_directory_exist():
        bus.call('kattcmd:init:directory-exists', folder)


    def is_partial_directory():
        missing_files = _FilesExist(files, get_missing=True)
        missing_dirs = _DirectoriesExist(dirs, get_missing=True)
        current_length = len(missing_files) + len(missing_dirs)
        expected_length = len(files) + len(dirs)
        return current_length != expected_length and current_length != 0


    def on_partial_exist():
        missing_files = _FilesExist(files, get_missing=True)
        missing_dirs = _DirectoriesExist(dirs, get_missing=True)
        missing = missing_files + missing_dirs
        expected = files + dirs
        bus.call('kattcmd:init:directory-partial', folder, expected, missing)


    def do_init():
        for dpath in dirs:
            os.mkdir(dpath)

        for fpath in files:
            with open(fpath, 'w') as f:
                pass

        bus.call('kattcmd:init:directory-created', folder)

    return pydash.cond([
        (is_kattcmd_already, on_directory_exist),
        (is_partial_directory, on_partial_exist),
        (pydash.stub_true, do_init)
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

