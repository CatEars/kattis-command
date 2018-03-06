import os
import tempfile

def with_custom_home(f):
    '''Descriptor for tests that should run in their own isolated environment.'''
    def inner(*args, **kwargs):
        with tempfile.TemporaryDirectory() as tempdirname:
            os.environ['HOME'] = tempdirname
            f(*args, **kwargs)

    return inner


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
