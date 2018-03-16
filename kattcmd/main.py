import click

from kattcmd import bus, core


@click.group()
def cli_main():
    '''Command line tool for solving kattis problems.

    kattcmd is a tool that tries to streamline solving kattis problems
    and make the user experience as pleasurable as possible for both
    newcomers and veterans.

    If you want to start working right away, then create a new
    directory somewhere fitting, move into it and run `kattcmd
    init`. This will initialize the directory as a kattcmd directory.
    Next up you want to make sure that you have a `.kattisrc` file. Go
    to https://YOURKATTISURL.com/download/kattisrc and follow the
    instructions there. After that you can open your problem with
    `kattcmd open PROBLEMID`, edit the file in `kattis/PROBLEMID` and
    then test and submit with `kattcmd test PROBLEMID` and `kattcmd
    submit PROBLEMID`, respectively.

    If you want more information about each command then run `kattcmd
    COMMAND --help`. If you want some quality of life improvements
    when using the tool (highly recommended!) then run `kattcmd tips`.

    If you find any problems or have suggestions then check out:
    https://git.lysator.liu.se/catears/kattis-command. There you will
    also find documentation with helpful usage cases and an FAQ.

    '''
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

    try:
        cli_main()
    except Exception as e:
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)


if __name__ == '__main__':
    main()
