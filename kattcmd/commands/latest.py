import os


class LatestError(Exception):
    pass


def _GetAcceptedExtensions():
    return _GetExtensions('python') + _GetExtensions('cpp')


def _GetExtensions(type):
    mapping = {
        'python': ['.py'],
        'cpp': ['.cc', '.cpp', '.cxx', '.h', '.hh', '.hpp', '.hxx']
    }
    return mapping[type]


def _GetFileType(extension):
    if extension in _GetExtensions('python'):
        return 'python'
    elif extension in _GetExtensions('cpp'):
        return 'cpp'
    else:
        return None


def GetLatest(bus, problemname):
    '''Returns the latest language type that was worked on in a problem
and the associated files.'''

    home = bus.call('kattcmd:find-root', bus)
    problempath = os.path.join(home, 'kattis', problemname)
    if not os.path.exists(problempath):
        bus.call('kattcmd:latest:no-files', problemname)
        return None

    items = [os.path.join(problempath, item) for item in os.listdir(problempath)]
    with_date = [(os.path.getmtime(fpath), fpath) for fpath in items]
    latest_first = reversed(sorted(with_date))
    accepted_exts = _GetAcceptedExtensions()

    # Filter latest first based on the accepted file extensions
    def IsAccepted(item):
        time, fpath = item
        return any(fpath.endswith(ext) for ext in accepted_exts)

    latest_first = list(filter(IsAccepted, latest_first))
    if len(latest_first) == 0:
        bus.call('kattcmd:latest:no-files', problemname)
        return None

    _, latest = latest_first[0]
    _, ext = os.path.splitext(latest)
    type = _GetFileType(ext)

    if not type:
        bus.call('kattcmd:latest:undetermined-extension', problemname, latest, ext)
        return None

    exts = _GetExtensions(type)
    def EndsInExt(fpath):
        return any(fpath.endswith(ext) for ext in exts)

    values = list(filter(EndsInExt, items))
    bus.call('kattcmd:latest:found', problemname, type, values)
    return type, values


def Init(bus):

    def OnNoFiles(problemname):
        '''Called if there are no files present in the folder.'''

    def OnUndeterminedExtension(problemname, fpath, ext):
        '''Called when an undetermined extesion is met.'''

    def OnItemsFound(problemname, type, fpaths):
        '''Called with the latest files and their determined type.'''

    bus.provide('kattcmd:latest:no-files', OnNoFiles)
    bus.provide('kattcmd:latest:found', OnItemsFound)
    bus.provide('kattcmd:latest:undetermined-extension', OnUndeterminedExtension)
    bus.provide('kattcmd:latest', GetLatest)
