# Writing a plugin

Basically every command you run with `kattcmd` is just a plugin that
comes with the default application. If you are writing a plugin then
you can simply look at the [files in the command folder](kattcmd/commands) to see how
to implement one. But in this tutorial I will walk you through
creating a simple plugin from scratch and hooking it up to
kattcmd. There will only be one major difference from the built-in
commands, and that is how your plugin is loaded, but now we are
getting ahead of ourselves.

# Goal

We want to create a simple script that moves a file in the `library`
folder into the problem folder we specify. In this tutorial you will
learn about important concepts used to create the `kattcmd` program
and how development for it works.

# Loading your plugin.

In order to properly load your plugin you will need two things, first
you will need to update your user config (`~/.kattcmd`) and the
`plugins` field in there so that there is a path pointing to your
plugin. Let's create some sample files that we can use to try this
out.

```bash
[~] $ mkdir plugin && cd plugin
[~/plugin] $ $EDITOR plugin.py
```

In order to load our plugin we need an `Init` method that takes a
single argument, the `bus`, which I will explain more about later
on. We will also want to create a function called `CLI`, which takes
two arguments, the `bus` and `parent`. We also want to include
`click`, which is what handles the command line interface for
us. Inside of `Init` we can add a print so that we know it it is
called or not.

```python
import click

def Init(bus):
    print('Hello!')

def CLI(bus, parent):
    pass
```

Now that we have our plugin, lets try and add it to the plugin path
and see if it is automatically imported or not.

```
[~/plugin] $ kattcmd setval --user plugins "[$(pwd/plugin.py)]"
```

