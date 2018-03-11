import os
import configparser
import click


def _SaveToConfigFile(configfile, key, value):
    config = configparser.ConfigParser()

    if os.path.exists(configfile):
        config.read(configfile)

    if not 'variables' in config:
        config['variables'] = {}

    if 'options' in config and key in config['options']:
        config['options'][key] = value
    else:
        config['variables'][key] = value

    with open(configfile, 'w') as f:
        config.write(f)


def _LoadFromConfigFile(configfile, key):
    try:
        config = configparser.ConfigParser()
        config.read(configfile)
        if 'options' in config and key in config['options']:
            return config['options'][key]

        if not 'variables' in config:
            config['variables'] = {}
        return config['variables'].get(key, None)
    except:
        return None


def _AddToConfig(bus, root, fname, topic, key, value):
    configfile = os.path.join(root, fname)
    _SaveToConfigFile(configfile, key, value)
    bus.call(topic, key, value)


def _LoadFromConfig(bus, root, fname, success_topic, fail_topic, key, default=None):
    configfile = os.path.join(root, fname)
    value = _LoadFromConfigFile(configfile, key)

    if value is None:
        bus.call(fail_topic, key)
        return default
    else:
        bus.call(success_topic, key, value)
        return value


def AddToRepoConfig(bus, key, value):
    '''Adds a key to the config of the current repo.'''
    _AddToConfig(
        bus=bus,
        fname='.kattcmddir',
        root=bus.call('kattcmd:find-root', bus),
        topic='kattcmd:config:add-repo-success',
        key=key,
        value=value
    )


def LoadFromRepoConfig(bus, key, default=None):
    '''Returns a value from the config of the current repo, or the deafult
value if not existing.'''
    return _LoadFromConfig(
        bus=bus,
        root=bus.call('kattcmd:find-root', bus),
        fname='.kattcmddir',
        success_topic='kattcmd:config:load-repo-success',
        fail_topic='kattcmd:config:load-repo-fail',
        key=key,
        default=default
    )


def AddToUserConfig(bus, key, value):
    '''Adds a key to the config of the user.'''
    _AddToConfig(
        bus=bus,
        fname='.kattcmd',
        root=os.path.expanduser('~'),
        topic='kattcmd:config:add-user-success',
        key=key,
        value=value
    )


def LoadFromUserConfig(bus, key, default=None):
    '''Loads a key from the config of the user.'''
    return _LoadFromConfig(
        bus=bus,
        root=os.path.expanduser('~'),
        fname='.kattcmd',
        success_topic='kattcmd:config:load-user-success',
        fail_topic='kattcmd:config:load-user-fail',
        key=key,
        default=default
    )


def Init(bus):

    def OnSuccessfulAddition(key, value):
        '''Event for when something was successfully added to a repo config.'''

    def OnFailAddition(key, value):
        '''Event for when adding something to a config failed.'''

    def OnSuccessfulLoad(key, value):
        '''Event for when a value was loaded successfully.'''

    def OnFailLoad(key):
        '''Event for when a value failed to load.'''

    bus.provide('kattcmd:config:add-repo', AddToRepoConfig)
    bus.provide('kattcmd:config:load-repo', LoadFromRepoConfig)
    bus.provide('kattcmd:config:add-user', AddToUserConfig)
    bus.provide('kattcmd:config:load-user', LoadFromUserConfig)

    bus.provide('kattcmd:config:add-repo-success', OnSuccessfulAddition)
    bus.provide('kattcmd:config:add-user-success', OnSuccessfulAddition)

    bus.provide('kattcmd:config:load-repo-success', OnSuccessfulLoad)
    bus.provide('kattcmd:config:load-user-success', OnSuccessfulLoad)
    bus.provide('kattcmd:config:load-repo-fail', OnFailLoad)
    bus.provide('kattcmd:config:load-user-fail', OnFailLoad)


def CLI(bus, parent):

    @click.command()
    @click.argument('key', type=str)
    @click.argument('value', type=str)
    @click.option('--user', default=False, type=bool, is_flag=True, help='Store value at user level')
    def setval(key, value, user):
        '''Sets a value in the config.

        Useful if you want to set your name or where your .kattisrc
        file is. Also useful for interacting with commands such as
        compile to customize your C++ compilation.

        See `kattcmd tips` for useful configuration values and how to
        set them.

        '''
        def OnSuccess(key, value):
            if user:
                click.echo('{}={} set in user config'.format(key, value))
            else:
                click.echo('{}={} set in repo config'.format(key, value))

        bus.listen('kattcmd:config:add-repo-success', OnSuccess)
        if user:
            bus.call('kattcmd:config:add-user', bus, key, value)
        else:
            bus.call('kattcmd:config:add-repo', bus, key, value)


    @click.command()
    @click.argument('key', type=str)
    @click.option('--user', default=False, type=bool, is_flag=True, help='Load value at user level')
    def getval(key, user):
        '''Prints value from the config.

        Useful if you want to inspect values in your config such as
        name or .kattisrc file.

        If the user flag is set it will look inside your user config,
        else it will try to find a config for the repo and print the
        value if it can find it there.

        '''
        if user:
            click.echo(bus.call('kattcmd:config:load-user', bus, key))
        else:
            click.echo(bus.call('kattcmd:config:load-repo', bus, key))


    parent.add_command(setval)
    parent.add_command(getval)
