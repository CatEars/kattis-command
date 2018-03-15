# Kattcmd open

This is the manual page for the command `kattcmd open PROBLEMNAME`

## Usage

```
$ kattcmd open carrots
...
$ kattcmd open funnygames
...
$ kattcmd open --force nonexistantproblemthatdoesntexist
```


## Effect

The `open` command is used to open and start working on a new
problem. The first and only argument is the problemid, as found on
kattis. `kattcmd` will automagically check that the problem exists on
kattis unless you use the flag `--force`, in which case it will open
the problem anyway.

`kattcmd` will start with checking that the problem exists. Then it
will create the folder and put your prefered template there. After
that it will try to download the sample tests and put them in the
`tests` directory. Note that there exists at least one problem on
kattis that does not have any sample input/output (but I think that it
is the only one).
