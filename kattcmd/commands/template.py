import os
import shutil


class TemplateError(Exception):
    pass


def _GetTemplateFolder():
    '''Returns the path to the template folder inside kattcmd.'''
    my_dir = os.path.dirname(__file__)
    path = os.path.join(my_dir, 'default_templates')
    return path


def _AddTemplate(templatename, extname, folder):
    '''Adds the designamed template to the folder with the extension.'''
    template = os.path.join(_GetTemplateFolder(), templatename)
    problemname = os.path.basename(folder) + extname
    templatepath = os.path.join(folder, problemname)
    shutil.copyfile(template, templatepath)
    return templatepath


def _HandleCustomTemplate(bus, fileend, folder):
    root = bus.call('kattcmd:find-root', bus)
    kattcmd_templates = os.path.join(root, 'templates')
    fnames = os.listdir(kattcmd_templates)
    is_py_file = lambda x: x.endswith(fileend)

    remaining = list(filter(is_py_file, fnames))
    if not remaining:
        msg = 'Could not find any templates in {} with "{}" ending'
        raise TemplateError(msg.format(kattcmd_templates, fileend))
    return _AddTemplate(remaining[0], fileend, folder)


def AddGeneralizedTemplate(bus, topic, folder, default, defaultname, fileending):
    '''Generalized handler for adding templates'''

    def HandleDefault():
        return _AddTemplate(defaultname, fileending, folder)

    def HandleCustom():
        return _HandleCustomTemplate(bus, fileending, folder)

    if default:
        path = HandleDefault()
    else:
        path = HandleCustom()

    bus.call(topic, folder, path)


def AddPython3Template(bus, folder, default=True):
    '''Adds a python3 template to a problem folder.'''
    return AddGeneralizedTemplate(
        bus=bus,
        topic='kattcmd:template:python-added',
        folder=folder,
        default=default,
        defaultname='py3.py',
        fileending='.py'
    )


def AddCppTemplate(bus, folder, default=True):
    '''Adds the default c++ template.'''
    return AddGeneralizedTemplate(
        bus=bus,
        topic='kattcmd:template:cpp-added',
        folder=folder,
        default=default,
        defaultname='cpp.cpp',
        fileending='.cpp'
    )


def Init(bus):

    def python_added(folder, templatepath):
        '''Event for adding a python template.'''

    def cpp_added(folder, templatepath):
        '''Event for adding a C++ template.'''

    bus.provide('kattcmd:template:python', AddPython3Template)
    bus.provide('kattcmd:template:cpp', AddCppTemplate)

    bus.provide('kattcmd:template:python-added', python_added)
    bus.provide('kattcmd:template:cpp-added', cpp_added)
