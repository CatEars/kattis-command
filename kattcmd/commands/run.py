import os
import subprocess
import click


def RunPythonAgainstTests(bus, inputs, problemname):
    '''Run python program against given inputs and return output/errors.'''
    home = bus.call('kattcmd:find-root', bus)
    executable = os.path.join(home, 'build', problemname, problemname + '.py')

    if not os.path.exists(executable):
        bus.call('kattcmd:run:no-executable', problemname, 'python')
        return

    timeout = bus.call('kattcmd:config:load-user', bus, 'default-timeout')
    timeout = timeout or bus.call('kattcmd:config:load-repo', bus, 'default-timeout')
    timeout = timeout or '10'
    timeout = int(timeout)

    def RunAgainstSingleInput(inputfile):
        abspath = os.path.abspath(inputfile)
        command = 'python {} < {}'.format(executable, abspath)
        try:
            output = subprocess.check_output(
                command,
                timeout=timeout,
                shell=True
            )
            if isinstance(output, bytes):
                output = output.decode('utf-8')
            return output
        except subprocess.TimeoutExpired as e:
            return e
        except subprocess.CalledProcessError as e:
            return e

    processes = [RunAgainstSingleInput(inputfile) for inputfile in inputs]
    bus.call('kattcmd:run:executed', problemname, 'python', inputs, processes)
    return processes


def RunCppAgainstTests(bus, inputs, problemname):
    '''Run c++ against given inputs and return outpu/errors.'''
    home = bus.call('kattcmd:find-root', bus)
    executable = os.path.join(home, 'build', problemname, problemname)

    if not os.path.exists(executable):
        bus.call('kattcmd:run:no-executable', problemname, 'cpp')
        return

    timeout = bus.call('kattcmd:config:load-user', bus, 'default-timeout')
    timeout = timeout or bus.call('kattcmd:config:load-repo', bus, 'default-timeout')
    timeout = int(timeout or '10')

    def RunSingleInput(inputfile):
        abspath = os.path.abspath(inputfile)
        command = '{} < {}'.format(os.path.abspath(executable), abspath)
        try:
            output = subprocess.check_output(
                command,
                timeout=timeout,
                shell=True
            )
            if isinstance(output, bytes):
                output = output.decode('utf-8')
            return output
        except subprocess.TimeoutExpired as e:
            return e
        except subprocess.CalledProcessError as e:
            return e

    processes = [RunSingleInput(inputfile) for inputfile in inputs]
    bus.call('kattcmd:run:executed', problemname, 'cpp', inputs, processes)
    return processes


def Init(bus):

    def OnNoExecutable(problemname, executable_type):
        '''Called when no executable could be found.'''

    def OnExecuted(problemname, executable_type, inputs, processes):
        '''Called when a problem has been executed and finished.'''

    bus.provide('kattcmd:run:python', RunPythonAgainstTests)
    bus.provide('kattcmd:run:cpp', RunCppAgainstTests)
    bus.provide('kattcmd:run:no-executable', OnNoExecutable)
    bus.provide('kattcmd:run:executed', OnExecuted)


