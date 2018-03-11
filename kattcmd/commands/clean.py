import click
import os
import shutil


def CleanBuildFolder(bus):
    '''Removes anything that exist in the buildfolder.'''
    home = bus.call('kattcmd:find-root', bus)
    build = os.path.join(home, 'build')
    items = [os.path.join(build, item) for item in os.listdir(build)]

    def RemoveSingle(fpath):
        shutil.rmtree(fpath, ignore_errors=True)
        return fpath

    values = list(map(RemoveSingle, items))
    bus.call('kattcmd:clean:completed', values)
    return values


def Init(bus):

    def OnCleanCompleted(directories):
        '''Event called when a clean was completed.'''

    bus.provide('kattcmd:clean:completed', OnCleanCompleted)
    bus.provide('kattcmd:clean', CleanBuildFolder)


def CLI(bus, parent):

    @parent.command()
    def clean():
        '''Cleans the build folder.

        Useful to do if your build folder is getting cluttered.

        Roughly equivalent to `rm -rf build/*`.

        '''
        items = bus.call('kattcmd:clean', bus)
        for item in items:
            path = os.path.relpath(item)
            click.secho('rm -rf {}'.format(path))

