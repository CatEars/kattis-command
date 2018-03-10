import os
import subprocess


def RunPythonAgainstTests(bus, inputs, problemname):
    '''Run python program against given inputs and return subprocesses/errors.'''
    home = bus.call('kattcmd:find-root')
    executable = os.path.join(home, 'build', problemname, problemname + '.py')

    if not os.path.exists(executable):
        bus.call('kattcmd:run:no-executable', problemname, 'python')
        return

    timeout = bus.call('kattcmd:config:load-user', bus, 'default-timeout')
    timeout |= bus.call('kattcmd:config:load-repo', bus, 'default-timeout')
    timeout |= '10'
    timeout = int(timeout)

    def RunAgainstSingleInput(inputfile):
        abspath = os.path.abspath(inputfile)
        with open(inputfile, 'r') as f:
            data = f.read()
        solution_folder = os.path.dirname(executable)
        command = 'python3 {}.py'.format(problemname)
        try:
            process = subprocess.run(
                command,
                timeout=timeout,
                cwd=solution_folder,
                input=str(data),
                encoding='utf-8'
            )
            return process
        except subprocess.TimeoutExpired as e:
            return e
        except CalledProcessError as e:
            return e
    processes = [RunAgainstSingleInput(inputfile) for inputfile in inputs]

    bus.call('kattcmd:run:executed', problemname, 'python', inputs, processes)
    return processes


def Init(bus):

    def OnNoExecutable(problemname, executable_type):
        '''Called when no executable could be found.'''

    def OnExecuted(problemname, executable_type, inputs, processes):
        '''Called when a problem has been executed and finished.'''

    bus.provide('kattcmd:run:python', RunPythonAgainstTests)
    bus.provide('kattcmd:run:no-executable', OnNoExecutable)
    bus.provide('kattcmd:run:executed', OnExecuted)

