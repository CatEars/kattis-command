import os

from .util import WithCustomHome, CallChecker
from kattcmd import core
from kattcmd import bus as busmodule
from kattcmd.commands import init, template


def DoTemplateTestWithType(topic, listen_topic, use_home=False, kwargs={}):
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
    if use_home:
        target = home
    else:
        target = os.path.join(home, 'kattis', 'hello')
        os.mkdir(target)

    bus.call(topic, bus, target, **kwargs)
    assert checker.yay
    assert os.listdir(target)



@WithCustomHome
def test_cpp_template():
    DoTemplateTestWithType('kattcmd:template:cpp',
                           'kattcmd:template:cpp-added',
                           kwargs={'default': True})
@WithCustomHome
def test_py_template():
    DoTemplateTestWithType('kattcmd:template:python',
                           'kattcmd:template:python-added',
                           kwargs={'default': True})
@WithCustomHome
def test_AllDefaultTemplate():
    DoTemplateTestWithType('kattcmd:template:default',
                           'kattcmd:template:default-added',
                           use_home=True)
