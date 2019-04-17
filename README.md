![tested with docker and pytest](https://img.shields.io/badge/tested%20with-docker%20%7C%20pytest-blue.svg)
![build status](https://travis-ci.org/CatEars/kattis-command.svg?branch=master)
[![saythanks](https://img.shields.io/badge/say-thanks-ffa500.svg?style=for-the-badge)](https://saythanks.io/to/CatEars)

# Kattis-Command

Tool for managing your competitive programming library and kattis solutions

Do you want to skip submitting manually to kattis? Do you want to have
a clean and nice structure for all your files when solving problems?
Are you willing to support and use community created tools?


## Main Goals

* Easy to install, easy to use

* Manage all non-programming related processes when working with Kattis

* Easily extendable with plugins


## Setup

Install through the use of pip. However you need to install it through
pip3, which may not be installed on your computer. If you have apt-get
installed you can run

```
$ sudo apt-get install python3-pip
```

After that you can install it with

```
pip3 install --user kattcmd
```

Or you can use `virtualenv`, but then you will need it whenever you
want to use `kattcmd`.

## Help I get "Command not found!"

If you have not configured to install with the `--user` flag before you might
need to add `~/local/.bin` to your path. The easiest way to do this is to append

```
export PATH=$PATH:~/.local/bin
```

to your `.bashrc` or `.zshrc` (if you are using bash/zsh respectively).

## Usage

See instructions on commands inside [docs](docs/index.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
