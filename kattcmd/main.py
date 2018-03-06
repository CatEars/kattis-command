import os
import pydash
import click

from kattcmd import doc, bus, core


def interactive_mode(bus, plugins):
    pass


def command_mode(bus, plugins, command):
    pass


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
        if hasattr(plugin, 'CLI'):
            plugin.CLI(the_bus, cli_main)

    cli_main()

    # # Check if interactive or not, if yes: run as interactive, if not then run command
    # if interactive:
    #     interactive_mode(the_bus, plugins)
    # elif not command:
    #     raise ValueError('Either you must specify a command or use interactive mode.')
    # else:
    #     command_mode(the_bus, plugins, command)


if __name__ == '__main__':
    main()
