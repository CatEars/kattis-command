import os
from random import randint

from .util import WithCustomCWD, WithMostModules, CallChecker

@WithCustomCWD
@WithMostModules
def test_AddToUserConfig(bus):
    home = os.environ['HOME']

    checker_success = CallChecker()
    checker_fail = CallChecker()
    number = str(randint(0, 10000))
    bus.listen('kattcmd:config:load-user-success', checker_success)
    bus.listen('kattcmd:config:load-user-fail', checker_fail)
    bus.call('kattcmd:config:add-user', bus, 'random', number)
    value = bus.call('kattcmd:config:load-user', bus, 'random')
    assert value == number
    assert checker_success.yay
    assert checker_fail.nay

    bus.call('kattcmd:config:load-user', bus, str(randint(0, 10000)))
    assert checker_fail.yay


@WithCustomCWD
@WithMostModules
def test_AddToRepoConfig(bus):
    home = os.environ['HOME']

    checker = CallChecker()
    bus.listen('kattcmd:init:directory-created', checker)
    bus.call('kattcmd:init', bus, home)
    assert checker.yay

    checker_success = CallChecker()
    checker_fail = CallChecker()
    number = str(randint(0, 10000))
    bus.listen('kattcmd:config:load-repo-success', checker_success)
    bus.listen('kattcmd:config:load-repo-fail', checker_fail)
    bus.call('kattcmd:config:add-repo', bus, 'random', number)
    value = bus.call('kattcmd:config:load-repo', bus, 'random')
    assert value == number
    assert checker_success.yay
    assert checker_fail.nay

    bus.call('kattcmd:config:load-repo', bus, str(randint(0, 10000)))
    assert checker_fail.yay
