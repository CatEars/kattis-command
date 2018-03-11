import click

from kattcmd import bus, core


@click.group()
def cli_main():
    pass


def main():
    '''Command line tool for helping with administrative tasks around Kattis.'''
    the_bus = bus.Bus()

    core.TouchStructure()
    plugins = core.ListPlugins()
    for plugin in plugins:
        plugin.Init(the_bus)

    for plugin in plugins:
        if hasattr(plugin, 'CLI'):
            plugin.CLI(the_bus, cli_main)

    cli_main()


if __name__ == '__main__':
    main()
