# Kattcmd compile

This is the manual page for `kattcmd compile PROBLEMNAME`

## Usage

```
$ kattcmd compile carrots
...
$ kattcmd compile funnygames
...
```

## Effect

The `compile` command is used to compile your solution and put it in
the `build` folder. It will look for a problem with the name you
specify on the command-line and try to compile that. When doing this
it will look for the most recently modified file and try to "compile"
it. In case it is an interpreted language it will simply copy the
necessary files to the `build` directory. In the `build` directory
each problem has it's own subfolder so, for example, the problem
`carrots` would store all it's files inside `build/carrots/`.

## Note

This command is not necessarily something you will use a lot. If you
run `test` then `kattcmd` will automatically compile the problem for
you so there is no need to run this command when testing. However, if
you have a kattis problem with complicated output/verification then
you may want to just `compile` and run it manually.
