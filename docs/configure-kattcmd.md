# Configure kattcmd with user values

This tutorial will walk you through manually setting configuration
values that will make your experience with `kattcmd` a little bit
better. This will be a shorter tutorial where most of the important
configuration values will be used. I will assume that you have created
a kattis folder using `kattcmd init` inside the `~/kattis` folder. I
will also go into small detail on how your commands change the state
of `kattcmd`.

Let's start!

# Changing our name

If you have opened a problem you may have noticied that `kattcmd` will
automatically enter a name for you into the template that is
automatically copied to the problem folder. But if you have not added
a name to your configuration then you might see `name: ZZZ`
somewhere. This is because `kattcmd` will automatically expand `ZZZ`
in templates to your name, or else just let it be `ZZZ` so that you
will wonder why it says `ZZZ` in the template and look at tutorials,
like this one. Lets assume that you have not yet `opened` the problem
`carrots` and run the following:

```bash
[~/kattis] $ kattcmd setval --user name "My Nahme"
[~/kattis] $ kattcmd open carrots
...
[~/kattis] $ $EDITOR kattis/carrots/carrots.py # Assuming a python template was created
```

You should now see that `My Nahme` was entered as the name instead of
`ZZZ`. Also if you now open `~/.kattcmd` you should see that you have
a field `"name": "My Nahme"` in there. Your `.kattcmd` holds important
configuration information and will hold any user value you add to it.

# Adding something useless

You can add anything you want to your `.kattcmd`, or the `.kattcmddir`
inside any repo and this allows for customization of plugins. If you
are a plugin developer and develop a plugin for `kattcmd` then you
can, without problem use configuration items from `.kattcmd` and
`.kattcmddir`. In fact, this is the intended use case of these
files. Let's try adding a value of no particular use and see what
happens.

```
[~/kattis] $ kattcmd setval dude "where is my car"
[~/kattis] $ kattcmd setval --user dude "not here!"
```

If we now check out `~/.kattcmd` and `~/kattis/.kattcmddir` we should
see that the `.kattcmddir` has `"dude": "where is my car"` in it,
while `.kattcmd` has `"dude": "not here!"` instead. Your user file is
global, so it will be visible over all repos. But the `.kattcmddir`
will be local to the repository and configuration items there will
only be used in that directory. Beware though that some configuration
items, such as `name`, needs to be in the user one.

# Changing default template and C++ compile command

Now lets do something actually useful. Let's make sure that `kattcmd`
will always use the `cpp.cpp` template instead of the `py3.py`
template. The value we want to change is the user-defined
`template-type` and the user-defined `cppcompile`. In order to change the
C++ compilation command we run

```
[~/kattis] $ kattcmd setval --user cppcompile "g++ -O2 FILES -o BINARY"
```

`FILES` and `BINARY` are values that will automatically get replaced
with the input source files and the output binary, respectively.

Now we just need to default to a C++ template. To do this run the
following command.

```
[~/kattis] $ kattcmd setval --user template-type "cpp"
```

valid values for `template-type` is `cpp` and `python`.

If you open a new problem you should see that your name is correctly
filled in, assuming you changed it from `My Nahme`. You should also
see that the file copied is a C++ file, not a python file. If you test
any problem it should also use your newly defined compilation command.

That is all for this tutorial. Hope you found it a little bit
interesting! If you want to look at a complete list of configuration
options you should head over to
the [manual for the getval/setval command](docs/getsetval.md).
