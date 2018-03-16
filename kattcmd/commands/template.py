import os
import shutil
import datetime


class TemplateError(Exception):
    pass


def _GetTemplateFolder():
    '''Returns the path to the template folder inside kattcmd.'''
    my_dir = os.path.dirname(__file__)
    path = os.path.join(my_dir, 'default_templates')
    return path


def _AddTemplate(templatepath, folder):
    '''Adds the designamed template to the folder with the extension.'''
    extname = os.path.splitext(templatepath)[1]
    problemname = os.path.basename(folder) + extname
    outputpath = os.path.join(folder, problemname)
    if not os.path.exists(outputpath):
        shutil.copyfile(templatepath, outputpath)
        return outputpath
    else:
        return None


def _ReplaceInFile(fpath, pattern, value):
    '''Replace pattern in the contents of fpath with value.'''
    with open(fpath, 'r') as f:
        data = f.read()
    data = data.replace(pattern, value)

    with open(fpath, 'w') as f:
        f.write(data)


def ReplaceFileWithInfo(bus, path):
    '''Replaces patterns inside the file with relevant data, such as authorname and date.'''
    folder = os.path.dirname(path)
    problemname = os.path.basename(folder)
    username = bus.call('kattcmd:config:load-user', bus, 'name', default='ZZZ')
    now = datetime.datetime.utcnow()
    datestr = str(now) + ' UTC'

    _ReplaceInFile(path, 'XXX', problemname)
    _ReplaceInFile(path, 'ZZZ', username)
    _ReplaceInFile(path, 'YYYY-MM-DD', datestr)

    bus.call('kattcmd:template:file-info-added', path)


def _HandleCustomTemplate(bus, fileend, folder):
    '''Uses a custom template in the kattis root folder.'''
    root = bus.call('kattcmd:find-root', bus)
    kattcmd_templates = os.path.join(root, 'templates')
    fnames = os.listdir(kattcmd_templates)
    is_X_file = lambda x: x.endswith(fileend)

    remaining = list(filter(is_X_file, fnames))
    if not remaining:
        msg = 'Could not find any templates in {} with "{}" ending'
        raise TemplateError(msg.format(kattcmd_templates, fileend))

    path = os.path.join(kattcmd_templates, remaining[0])
    return _AddTemplate(path, folder)


def AddGeneralizedTemplate(bus, topic, folder, fileending, default, defaultname):
    '''Generalized handler for adding templates'''

    def HandleDefault():
        templatefolder = _GetTemplateFolder()
        defaultpath = os.path.join(templatefolder, defaultname)
        return _AddTemplate(defaultpath, folder)

    def HandleCustom():
        return _HandleCustomTemplate(bus, fileending, folder)

    if default:
        path = HandleDefault()
    else:
        path = HandleCustom()
    
    bus.call(topic, folder, path)
    return path


def AddPython3Template(bus, folder, default=False):
    '''Adds a python3 template to a problem folder.'''
    return AddGeneralizedTemplate(
        bus=bus,
        topic='kattcmd:template:python-added',
        folder=folder,
        default=default,
        defaultname='py3.py',
        fileending='.py'
    )


def AddCppTemplate(bus, folder, default=False):
    '''Adds the default c++ template.'''
    return AddGeneralizedTemplate(
        bus=bus,
        topic='kattcmd:template:cpp-added',
        folder=folder,
        default=default,
        defaultname='cpp.cpp',
        fileending='.cpp'
    )


def AddAllDefaultTemplates(bus, katthome):
    '''Adds all default templates to the templates folder.'''
    def AddTemplate(templatename):
        source = os.path.join(_GetTemplateFolder(), templatename)
        target = os.path.join(katthome, 'templates', templatename)
        shutil.copyfile(source, target)
    AddTemplate('py3.py')
    AddTemplate('cpp.cpp')
    bus.call('kattcmd:template:default-added', os.path.join(katthome, 'templates'))


def Init(bus):

    def PythonAdded(folder, templatepath):
        '''Event for adding a python template.'''

    def CppAdded(folder, templatepath):
        '''Event for adding a C++ template.'''

    def OnFileInfoAdded(path):
        '''Event for changing info in file with default info.'''

    def OnAllDefaultAdded(path):
        '''Event for when all default templates are added to a folder.'''

    bus.provide('kattcmd:template:python', AddPython3Template)
    bus.provide('kattcmd:template:cpp', AddCppTemplate)
    bus.provide('kattcmd:template:default', AddAllDefaultTemplates)

    bus.provide('kattcmd:template:python-added', PythonAdded)
    bus.provide('kattcmd:template:cpp-added', CppAdded)
    bus.provide('kattcmd:template:default-added', OnAllDefaultAdded)

    bus.provide('kattcmd:template:add-info', ReplaceFileWithInfo)
    bus.provide('kattcmd:template:file-info-added', OnFileInfoAdded)

