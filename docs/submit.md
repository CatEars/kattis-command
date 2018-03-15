# Kattcmd submit

This is the manual page for the command `kattcmd submit PROBLEMNAME`

## Usage

```
$ kattcmd submit carrots
...
$ kattcmd submit funnygames
```

## Effect

The `submit` command is used when you think that your solution to a
problem is correct and want to submit it to kattis. It will find all
the relevant files to upload and try to submit it to kattis. Then it
will open the submission in your browser so that you can see the
progress, or any eventual error that may arise.

In order to run this command you will need to have downloaded a
`.kattisrc` file and put it in your home folder as `~/.kattisrc`. If
you go into your kattis instance (for example [open](https://open.kattis.com) or [liu](https://liu.kattis.com))
and into the `help` tab, then click on the `How to submit` link. In
here you will have a link `Download your personal configuration
file`. Click on that and download the file as `~/.kattisrc`. The file
includes a *personal* access token, which means you should make sure
only you can read/write to it. This can be done with `chmod 600
~/.kattisrc` on most UNIX-like systems.
