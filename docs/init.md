# Kattcmd init

This is the manual page for the command `kattcmd init`

## Usage

```
$ kattcmd init
```


## Effect

The `init` command is used to initialize a new kattis directory, a
folder in which you can implement solutions to kattis problems. In
order to run most commands of `kattcmd` you will need to be inside a
folder (or subfolder) of a kattis directory.

You can compare this command to `git init`, which initializes the
current directory as a git directory and only once you have done this
can you use other git commands, such as `git add` or `git
log`. `kattcmd init` is similar in that it is the first command you
run in order to use `kattcmd` effectively.

By running `kattcmd init` you will also create 5 folder, `library`,
`templates`, `kattis`, `tests` and `build`. Each one of these has a
use in the `kattcmd` ecosystem.

* `library` - Where you keep your code library. General algorithms and
  such should be placed here. Items such as `graph.py` or
  `sorting.hpp` are relevant files to put here. `kattcmd` has no
  command that use this folder, but it creates this because having a
  code library that can solve general problems is essential to
  competitive programming.
  
* `templates` - Where all the templates are kept. Initially only has
  `py3.py` and `cpp.cpp` which is a python3 and C++ template,
  respectively. These will be copied into any problem you open
  (depending on your language preference) and can be freely
  edited. However you need to keep the filenames like they are or
  `kattcmd` will not find them.
  
* `kattis` - Where all your solutions will be. Whenever you open a new
  problem, `kattcmd` will create a folder for it here and move a
  template to it. For example the problem `carrots` will be put inside
  `kattis/carrots/` and if you have python as your language preference
  then you will have `kattis/carrots/carrots.py`.
  
* `tests` - Contains tests for different kattis problems. If you open
  a new problem then `kattcmd` automatically downloads the sample
  input/output and puts them inside the `tests` folder. For the
  problem `carrots` it will create the folder `tests/carrots` and put
  them there. Note that `kattcmd` uses filenames for tests to
  determine which test-input to pair with what test-output. If the
  file is named `X.in` then `kattcmd` will look for `X.ans` and if it
  is `carrots.01.in` `kattcmd` will look for `carrots.01.ans`
  
* `build` - Contains your compiled binaries or tested
  scripts. Whenever `kattcmd` tests or compiles your solution it will
  create a runnable executable (or runnable script) inside the `build`
  folder. This is to make version control easy and separate
  implementation source code from runnable executables. If you want to
  manually run a program you can find them in the `build` folder. For
  example if you have solved `carrots` with a C++ program then the
  output binary will be `build/carrots/carrots`.


