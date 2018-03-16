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
plugin. We will not update this manually as you can add a plugin here
with `kattcmd plugin --add`. But for now let's create some sample
files that we can use to try this out.

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

```bash
[~/plugin] $ kattcmd plugin --add plugin.py
[~/plugin] $ kattcmd plugin --list
Hello!
Plugins:
   - plugin@...../plugin.py
```

If your plugin was loaded correctly you should see something similar
to the above. As you can see our message in `Init` was printed. From
here on out it is just to start developing whatever you find fancy!

But we need to go a bit deeper into how to do things. The most
important thing you will use is the `bus`.

# The bus

The bus is the main way of communication for the application. It is
basically an event handler and Remote Procedure Call (RPC) manager in
one. [It is surprisingly easy to write one!](kattcmd/bus.py) When a builtin command
is loaded in `Init` it will only do one of two things. (1) define a
function. (2) call `Bus.provide(topic, handler)`. You should follow
this style as well if you are providing functions to the bus! What you
might want to do is listen to other RPC calls, but we will not go into
further discussion on that now. Today we want to use things that are
already registered on the bus and our main goal is to create the
`libcp` command. Some things that we will need to know is the repo the
user is in. This can be gotten with the topic `kattcmd:find-root` from
the bus. The call would look like the following:

```python
home = bus.call('kattcmd:find-root', bus)
```

Of course we might want to guard ourselves in case the user is not in
the a kattis repository.

```python
try:
    home = bus.call('kattcmd:find-root', bus)
except Exception as e:
    print('User is not in a kattis directory', e)
    exit(1)
```

We will also need to copy a file in the `library` to our solution
folder. Here is the basic gist of what we want to do.

```python
try:
    home = bus.call('kattcmd:find-root', bus)
except Exception as e:
    print('User is not in a kattis directory', e)
    exit(1)

library_file = '...'
problem_name = '...'

src = os.path.join(home, 'library', library_file)
dst = os.path.join(home, 'kattis', problem_name, library_file)
shutil.copyfile(src, dst)
```

Obviously we want `library_file` and `problem_name` to be specified by
the user, and for this we will use [click](http://click.pocoo.org/5/). `parent` inside the
`CLI` function is a click `Group`, which means it has a lot of
subcommands. In order to specify library file and problem name we
could do the following.

```python

def CLI(bus, parent):
    @parent.command()
    @click.argument('libfile')
    @click.argument('problem')
    def libcp(libfile, problem):
        pass
```

Now we have created the command `kattcmd libcp LIBFILE PROBLEM`. Both passed as
strings to the `libcp` function.
