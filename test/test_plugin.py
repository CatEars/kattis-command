import os

from .util import WithMostModules, WithCustomCWD, ExecuteInOrder


PLUGIN = """
def Init(bus):
    pass
"""

@WithCustomCWD
@WithMostModules
def test_AddAndRemovePlugin(bus):
    path = os.path.abspath('coolplugin.py')
    with open(path, 'w') as f:
        f.write(PLUGIN)
    calls = [
        ('kattcmd:plugin:add', 'kattcmd:plugin:plugin-loaded', [path]),
        ('kattcmd:plugin:list', 'kattcmd:plugin:plugins-listed'),
        ('kattcmd:plugin:remove', 'kattcmd:plugin:plugins-updated', ['cool'])
    ]
    items = list(ExecuteInOrder(bus, calls))
    assert all(checker.yay for _, checker in items)
    results = [result for result, _ in items]
    assert len(results) == 3

    plugin_path, loaded_plugins, updated_plugins = results
    assert plugin_path == path

    assert loaded_plugins[0][0] == 'success'

    assert updated_plugins[0] == []
    assert updated_plugins[1] == [path]
    
