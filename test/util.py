import os
import tempfile
from kattcmd import core
from kattcmd import bus as busmodule
from kattcmd.commands import open as open_command, compile as compile_command, \
    init, root, config, template, test_download, test, run, clean, submit

def WithCustomCWD(f):
    '''Descriptor for tests that should run in an isolated environment.'''
    def inner(*args, **kwargs):
        with tempfile.TemporaryDirectory() as tempdirname:
            os.environ['HOME'] = tempdirname
            old_cwd = os.getcwd()
            os.chdir(tempdirname)

            try:
                f(*args, **kwargs)
            finally:
                os.chdir(old_cwd)
    return inner


def WithCustomHome(f):
    '''Descriptor for tests that should run with special HOME variable.'''
    def inner(*args, **kwargs):
        with tempfile.TemporaryDirectory() as tempdirname:
            os.environ['HOME'] = tempdirname
            f(*args, **kwargs)

    return inner


def WithModules(modulelist):
    def wrapper(f):
        def inner(*args, **kwargs):
            if not 'HOME' in os.environ or not os.environ['HOME'].startswith('/tmp'):
                print(os.environ['HOME'])
                print('*'*42)
                print('HOME NOT SET IN test.util.with_modules()! Make sure to put @with_modules innermost')
                print('*'*42)

            if not core.TouchStructure():
                raise AssertionError('Could not create home structure!')

            bus = busmodule.Bus()
            for module in modulelist:
                module.Init(bus)

            f(bus, *args, **kwargs)
        return inner

    return wrapper


def WithMostModules(f):
    return WithModules([
        init, root, config, template, test_download, open_command, compile_command, test,
        run, clean, submit
    ])(f)


class CallChecker:

    def __init__(self):
        self.is_called = False

    def __call__(self, *args, **kwargs):
        self.is_called = True

    @property
    def yay(self):
        return self.is_called

    @property
    def nay(self):
        return not self.is_called


def ExecuteRPC(bus, topic, answertopic, *args, **kwargs):
    checker = CallChecker()
    bus.listen(answertopic, checker)
    result = bus.call(topic, *args, **kwargs)
    return result, checker


def RunWithChecker(bus, topic, answertopic, *args, **kwargs):
    return ExecuteRPC(bus, topic, answertopic, *args, **kwargs)[1]


def ExecuteInOrder(bus, calls):
    for item in calls:
        topic, answertopic = item[:2]
        arguments = []
        kwargs = {}
        if len(item) >= 3:
            arguments = item[2]
        if len(item) >= 4:
            kwargs = item[3]

        checker = CallChecker()
        bus.listen(answertopic, checker)
        result = bus.call(topic, bus, *arguments, **kwargs)
        yield result, checker
