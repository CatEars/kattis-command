import click
import os
import importlib.util
import pydash
import ast

from kattcmd import core


def _AddPluginInConfig(bus, path):
    '''Adds plugin to user config.'''
    plugins = bus.call('kattcmd:config:load-user', bus, 'plugins')
    plugins = ast.literal_eval(plugins)
    plugins.append(path)
    plugins = list(set(plugins))
    bus.call('kattcmd:config:add-user', bus, 'plugins', str(plugins))


def AddPlugin(bus, path):
    '''Checks the plugin at path and adds it to user config.'''
    type, value = core.ImportExternal(path)


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
    '''Returns a list of all the plugins, as returned by ImportExternal.'''
    plugins = ast.literal_eval(bus.call('kattcmd:config:load-user', bus, 'plugins'))
    values = list(map(core.ImportExternal, plugins))
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

    def _ToPluginName(path):
        basename = os.path.basename(path)
        name, ext = os.path.splitext(basename)
        return name

    def OnBadExtension(path):
        click.secho('plugin {} has a bad extension, skipping'.format(path), fg='red')
        click.secho('To make this go away, please remove the plugin with:', fg='red')

        remove_command = 'kattcmd plugin --remove {}'.format(path)
        click.echo('   {}'.format(remove_command))

    def OnImportError(path, error):
        click.secho('plugin {} could not be imported, skipping'.format(path), fg='red')
        click.echo('Error text:')
        click.echo(str(error))

    def OnPluginLoaded(path):
        name = _ToPluginName(path)
        click.echo('plugin {} added'.format(name))

    def OnPluginsUpdated(new_plugins, removed_plugins):
        click.echo('Removed:')
        for path in removed_plugins:
            name = _ToPluginName(path)
            click.echo('   - {}'.format(name))

        click.echo('Plugins still active: ')
        for path in new_plugins:
            name = _ToPluginName(path)
            click.echo('   - {}'.format(name))

    def OnPluginsListed(plugins):
        if not plugins:
            click.echo('No plugins installed')
            return

        click.echo('Plugins:')
        for type, value in plugins:
            if type == 'success':
                path = value.__name__
                name = _ToPluginName(path)
                click.echo('   - {}@{}'.format(name, path + '.py'))
            elif type == 'extension':
                path, extension = value
                click.secho('   - {} (Error: bad extension: {})'.format(path, extension), fg='red')
            elif type == 'error':
                path, error = value
                click.secho('   - {} (Error: import error)'.format(path), fg='red')
                if os.getenv('DETAILED_ERROR'):
                    click.secho('        {}'.format(str(error)), fg='red')


    @parent.command()
    @click.option('--add', type=str, help='Add plugin so that it is loaded into kattcmd.', default=None)
    @click.option('--remove', type=str, help='Remove any plugin that matches the string after --remove.', default=None)
    @click.option('--match-path', is_flag=True, help='Used with --remove to indicate that the pattern should match against the full path of the plugin.', default=False)
    @click.option('--list', is_flag=True, help='Lists the different plugins that are loaded.', default=False)
    @click.option('--detailed-error', is_flag=True, help='Displays details of any import errors')
    def plugin(add, remove, match_path, list, detailed_error):
        '''Add/Remove/List plugins.

        Use either the `--add STR` to add a plugin, or the `--remove
        STR` to remove a plugin matching STR or `--list` to list
        installed plugins.

        --match-path is used with --remove and will make the pattern
        match the whole path, and just not the filename.

        --detailed-error is used with --list and will print a detailed
          import error for any plugin that was not imported correctly.

        '''
        bus.listen('kattcmd:plugin:bad-extension', OnBadExtension)
        bus.listen('kattcmd:plugin:import-error', OnImportError)
        bus.listen('kattcmd:plugin:plugin-loaded', OnPluginLoaded)
        bus.listen('kattcmd:plugin:plugins-updated', OnPluginsUpdated)
        bus.listen('kattcmd:plugin:plugins-listed', OnPluginsListed)

        if detailed_error:
            os.environ['DETAILED_ERROR'] = '1'

        if add:
            add = os.path.abspath(add)
            bus.call('kattcmd:plugin:add', bus, add)
        elif remove:
            bus.call('kattcmd:plugin:remove', bus, remove, match_path=match_path)
        elif list:
            bus.call('kattcmd:plugin:list', bus)
        else:
            with click.Context(plugin) as ctx:
                click.echo(plugin.get_help(ctx))
