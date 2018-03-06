import os

from .util import with_custom_home, CallChecker
from kattcmd import core
from kattcmd import bus as busmodule
from kattcmd.commands import init, template


def do_template_test_with_type(topic, listen_topic):
    assert core.TouchStructure()
    checker = CallChecker()

    bus = busmodule.Bus()
    init.Init(bus)
    template.Init(bus)

    bus.listen('kattcmd:init:directory-created', checker)

    home = os.environ['HOME']
    bus.call('kattcmd:init', bus, folder=home)
    assert checker.yay

    checker = CallChecker()
    bus.listen(listen_topic, checker)
    target = os.path.join(home, 'kattis', 'hello')
    os.mkdir(target)

    bus.call(topic, bus, target)
    assert checker.yay
    assert os.listdir(target)



@with_custom_home
def test_cpp_template():
    do_template_test_with_type('kattcmd:template:cpp',
                               'kattcmd:template:cpp-added')
@with_custom_home
def test_py_template():
    do_template_test_with_type('kattcmd:template:python',
                               'kattcmd:template:python-added')
