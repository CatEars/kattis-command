# Kattcmd getval/Kattcmd setval

This is the manual page for the commands `kattcmd setval KEY VALUE`
and `kattcmd getval KEY`.

## Usage

```
$ kattcmd getval --user name
...
$ kattcmd setval --user name "catears"
...
$ kattcmd setval mykey myvalue
```

## Effect

The `getval` command will display the value of a configuration
item. It is used to check the value of a certain key. If you use the
`--user` flag it will look at user-defined values instead of
repo-defined values.

The `setval` command is used to set values so that `kattcmd` can be
configured to your liking. If you use the `--user` flag it will save
to the user-defined values instead of the repo-defined values.

## List of configuration options

Explanation; Each configuration option looks like this:

* `key`: (user/repo) explanation of usage
  * `Example command`

The key is the key for the configuration item. (user/repo) will show
if the value is user-defined or repo-defined (if you need to supply
the `--user` flag or not). If both are possible then it will say
(user/repo). "explanation of usage" is a one-sententence explanation of
what the command does and `Example command` is a runnable command that
changes the value.

* `kattisrc`: (user) Path to the user's `.kattisrc`
  * `kattcmd setval --user kattisrc "$(pwd)/.kattisrc"`
  
* `plugins`: (user) List of paths to plugins available. Not intended to be touched by `setval`
  * `kattcmd setval --user plugins "[$(pwd)/myplugin.py]"`
  
* `cppcompile`: (user) Command to run when compiling C++ sources. Replaces `FILES` with sources and `BINARY` with output binary name.
  * `kattcmd setval --user cppcompile "g++ -std=c++17 FILES -o BINARY"`
  
* `template-type`: (user) Type of template to load by default when opening a new problem. Accepted values: ['python', 'cpp'].
  * `kattcmd setval --user template-type "cpp"`
  
* `default-kattis`: (user) Path to default kattis repo to operate in. If this is set then kattis will fall back to working with that, if you are not in a subfolder of a kattis directory.
  * `kattcmd setval --user default-kattis /home/myname/Documents/kattis-solutions`
  
* `default-timeout`: (user/repo) The timeout, in seconds, for a single test to be terminated.
  * `kattcmd setval default-timeout 1`
  
* `name`: (user) Used when opening a new template. `ZZZ` is expanded to this value on opening a problem.
  * `kattcmd setval --user name "Person Mc personsen"`
