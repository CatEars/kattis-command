from .util import WithCustomCWD, WithMostModules, ExpectFileSystem
import os
from collections import namedtuple


CallConfig = namedtuple('CallConfig', 'call exist nonexist')


def MakeCaller(systemcall):
    return lambda: os.system(systemcall)


def FromRoot(path):
    home = os.environ['HOME']
    return os.path.join(home, path)


@WithCustomCWD
@WithMostModules
def test_SimpleStory(bus):

    P = FromRoot
    C = MakeCaller
    # The following operations are performed, in that order:

    # kattcmd init
    # kattcmd setval --user template-type python
    # kattcmd open carrots
    # kattcmd test carrots
    # kattcmd clean
    # kattcmd compile carrots
    # kattcmd setval --user template-type cpp
    # kattcmd open funnygames
    # kattcmd compile funnygames

    # items is an array of tuples
    items = [
        CallConfig(
            MakeCaller('kattcmd init'),
            [
                P('kattis'),
                P('library'),
                P('templates'),
                P('templates/py3.py'),
                P('templates/cpp.cpp'),
                P('build'),
                P('tests')
            ],
            []
        ),

        CallConfig(
            MakeCaller('kattcmd setval --user template-type python'),
            [],
            []
        ),

        CallConfig(
            MakeCaller('kattcmd open carrots'),
            [
                P('kattis/carrots/carrots.py'),
                P('tests/carrots')
            ],
            []
        ),

        CallConfig(
            MakeCaller('kattcmd test carrots'),
            [
                P('build/carrots'),
                P('build/carrots/carrots.py')
            ],
            []
        ),

        CallConfig(
            MakeCaller('kattcmd clean'),
            [],
            [
                P('build/carrots/carrots.py'),
                P('build/carrots')
            ]
        ),

        CallConfig(
            MakeCaller('kattcmd compile carrots'),
            [
                P('build/carrots'),
                P('build/carrots/carrots.py')
            ],
            []
        ),

        CallConfig(
            MakeCaller('kattcmd setval --user template-type cpp'),
            [],
            []
        ),

        CallConfig(
            MakeCaller('kattcmd open funnygames'),
            [
                P('kattis/funnygames'),
                P('kattis/funnygames/funnygames.cpp')
            ],
            []
        ),

        CallConfig(
            MakeCaller('kattcmd compile funnygames'),
            [
                P('build/funnygames'),
                P('build/funnygames/funnygames')
            ],
            []
        )
    ]

    calls = [item.call for item in items]
    existing_files = [item.exist for item in items]
    non_existing_files = [item.nonexist for item in items]
    files = ExpectFileSystem(calls, os.environ['HOME'])

    for actual, expect, nonexpect in zip(files, existing_files, non_existing_files):
        for e in expect:
            assert e in actual
        for n in nonexpect:
            assert n not in actual
