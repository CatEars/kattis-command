import os
import tempfile
from kattcmd import core
from kattcmd import bus as busmodule

def WithCustomHome(f):
    '''Descriptor for tests that should run in their own isolated environment.'''
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
