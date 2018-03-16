import click
import os
import importlib.util
import pydash
import ast

def _ToPlugin(path):
    '''Checks that path is a plugin.'''
    name, extension = os.path.splitext(path)
    if extension != '.py':
        return ('extension', None)
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return ('success', module)
    except ImportError as e:
        return ('error', e)


def _AddPluginInConfig(bus, path):
    '''Adds plugin to user config.'''
    plugins = bus.call('kattcmd:config:load-user', bus, 'plugins')
    plugins = ast.literal_eval(plugins)
    plugins.append(path)
    plugins = list(set(plugins))
    bus.call('kattcmd:config:add-user', bus, 'plugins', str(plugins))
    

def AddPlugin(bus, path):
    '''Checks the plugin at path and adds it to user config.'''
    type, value = _ToPlugin(path)


    def IsBadExtension():
        return type == 'extension'

    def HandleBadExtension():
        bus.call('kattcmd:plugin:bad-extension', path)
    

    def IsImportError():
        return type == 'error'

    def HandleImportError():
        bus.call('kattcmd:plugin:import-error', path, value)


    def HandleNormalCase():
        _AddPluginInConfig(bus, path)
        bus.call('kattcmd:plugin:plugin-loaded', path)
        return path

    return pydash.cond([
        (IsBadExtension, HandleBadExtension),
        (IsImportError, HandleImportError),
        (pydash.stub_true, HandleNormalCase)
    ])()


def RemovePlugin(bus, pattern, match_path=False):
    '''Removes any plugin matching the pattern in its basename, unless matches against path.'''
    plugins = ast.literal_eval(bus.call('kattcmd:config:load-user', bus, 'plugins'))

    def DoSave(new_plugins):
        removed = list(sorted(set(plugins) - set(new_plugins)))
        bus.call('kattcmd:config:add-user', bus, 'plugins', str(new_plugins))
        bus.call('kattcmd:plugin:plugins-updated', new_plugins, removed)
        return new_plugins, removed

    def ShouldMatchAgainstPath():
        return match_path

    def HandleMatchPath():
        new_plugins = list(filter(lambda x: pattern not in x, plugins))
        return DoSave(new_plugins)


    def ShouldMatchAgainstBase():
        return not match_path

    def HandleMatchBase():
        new_plugins = list(filter(lambda x: pattern not in os.path.basename(x), plugins))
        return DoSave(new_plugins)


    return pydash.cond([
        (ShouldMatchAgainstBase, HandleMatchBase),
        (ShouldMatchAgainstPath, HandleMatchPath)
    ])()


def ListPlugins(bus):
    '''Returns a list of all the plugins, as returned by _ToPlugin.'''
    plugins = ast.literal_eval(bus.call('kattcmd:config:load-user', bus, 'plugins'))
    values = list(map(_ToPlugin, plugins))
    bus.call('kattcmd:plugin:plugins-listed', values)
    return values


def Init(bus):

    def OnBadExtension(path):
        '''Called when a plugin has a bad extension (not .py).'''

    def OnImportError(path, error):
        '''Called when a plugin could not properly be imported.'''

    def OnPluginLoaded(path):
        '''Called when a plugin was successfully loaded.'''

    def OnPluginsUpdated(new_plugins, removed_plugins):
        '''Called when a plugins were updated.'''

    def OnPluginsListed(plugins):
        '''Called when plugins are listed.'''

    bus.provide('kattcmd:plugin:bad-extension', OnBadExtension)
    bus.provide('kattcmd:plugin:import-error', OnImportError)
    bus.provide('kattcmd:plugin:plugin-loaded', OnPluginLoaded)
    bus.provide('kattcmd:plugin:add', AddPlugin)

    bus.provide('kattcmd:plugin:plugins-updated', OnPluginsUpdated)
    bus.provide('kattcmd:plugin:remove', RemovePlugin)

    bus.provide('kattcmd:plugin:plugins-listed', OnPluginsListed)
    bus.provide('kattcmd:plugin:list', ListPlugins)


def CLI(bus, parent):
    pass
