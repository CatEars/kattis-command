# Kattcmd test

This is the manual page for the command `kattcmd test PROBLEMNAME`

## Usage

```
$ kattcmd test carrots
...
$ kattcmd test funnygames
...
```

## Effect

The `test` command is used to test your solution to a problem. It will
automatically [compile](compile.md) your solution, and then run it against the
tests it can find in the `tests` folder. If you have multiple
solutions it will look at the files that were modified most recently
and try to figure out what language you want to run it in.

On running your solution against the testdata, `kattcmd` will print a
diff between the expected output (the corresponding `.ans` file) and
this uses the [python difflib](https://docs.python.org/3/library/difflib.html) in order to diff the output and the
expected output. One unfortunate consequence of this is that some
problems that are harder to verify may be reported as Wrong Answer
when kattis might give you Accepted. In these complicated cases it may
be a good idea to test the problem manually.

In order to add your own tests and make `kattcmd` use them, you will
need to add them to the correct test folder and give them the correct
name. For example, if you have an input file `myinput.txt` and
`myoutput.txt` and these are manually verified tests for the problem
`carrots`. Then you can copy `myinput.txt` to
`tests/carrots/mytest.in`, copy `myoutput.txt` to
`tests/carrots/mytest.ans` and `kattcmd` will use the testcase
`mytest.in` while testing and compare it to `mytest.ans`.
