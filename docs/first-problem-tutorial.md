# Submit your first problem with kattcmd

Welcome to the tutorial on on submitting your first problem to kattis
with kattcmd. In this tutorial we will do the following:

* Create a directory for you to work with your kattis problems

* Open and start working on a new problem (carrots)

* Test our solution against the sample data

* Submit the problem to kattis

Let's get started!

# Setup and directory

I will assume that you have installed `kattcmd` on your computer and
that you can run it in the terminal. I will also assume that you have
downloaded the `.kattisrc` file from your particular kattis
instance. If not, then you should be able to go into the "help" tab
and find the "How to Submit" link. In there you should be able to find
a link to download your personal configuration file. On
[open.kattis.com](https://open.kattis.com) this page can be found at
[https://open.kattis.com/help/submit](https://open.kattis.com/help/submit).
Follow the instructions there to download the configuration file, it
is necessary for submitting problems to kattis. After that is done we
want to continue with the actual tutorial!

First you want to create a completely new folder where you will be
storing all your solutions.

```
[~] $ mkdir kattis
[~] $ cd kattis
[~/kattis] $ kattcmd init
kattcmd folder initialized.
Added all default templates to: templates
Happy Coding!
[~/kattis] $ ls
build  kattis  library  templates  tests
```

Now we have created our folder with all necessary parts. The `build`
folder will contain compiled binaries or (if you use an interpreted
language) will be holding your solution scripts. If you ever want to
manually run a program, you can run it from there. For example if you
implement a solution to the "carrots" problem you can run
`./build/carrots/carrots` from `~/kattis` and you will run your
program like normally.

The `kattis` folder will include your solutions to the
problems. Whenever you open a new problem with `kattcmd open` you will
find that a template file will be copied to the problem folder, for
example `~/kattis/kattis/carrots`. Try to keep your solutions in that
folder and that folder only.

The `library` folder is created and the idea is that sometimes you
find very general algorithms, such as Dijkstra's algorithm or Dinic's
Max-Flow algorithm. It is beneficial to keep these separate from your
kattis solutions, as they are very general and can usually stand on
their own. One important thing tough is that `kattcmd` will not
automatically include the things in your library, so you will need to
copy things from your library into the correct kattis folder. I've
found that the process is often the reverse tough. You create a
solution for a problem and realize that the solution is quite general
and could easily be applied to something else.

The `templates` folder contains templates that are automatically
copied into any new problem. Feel free to change them to your liking,
just make sure to keep the same name!

The `tests` folder includes all your tests to problems and `kattcmd
open` will automagically download any sample tests and put them there
for you. To create your own test you need to create a file that ends
with `.in` and a matching file that ends with `.ans`. For example if I
create `myexample.in` then the corresponding file would be
`myexample.ans`. Unfortunately `kattcmd` does not handle programmatic
comparison of answers, only diffing. This means that if you output `1
2 3`, the answer file says `3 2 1` and that the order of the number
does not matter. Then `kattcmd` will report that you did something
wrong. Keep this in mind when testing your solution!

Next up we are gonna solve an actual problem.

# Opening the carrots problem

Start up by opening the problem using `kattcmd open`

```
[~/kattis] $ kattcmd open carrots
Opened carrots for solving
Tests put inside of tests/carrots
[~/kattis] $ ls kattis/carrots
carrots.py
[~/kattis] $ ls tests/carrots
carrots.01.ans  carrots.01.in  carrots.02.ans  carrots.02.in
```

Using `kattcmd open carrots` "opened" a new problem. That means it
created the folder in `kattis`, put the python template there and
named it `carrots.py`. Lets try out testing it right now, without any
implementation!

```
[~/kattis] $ kattcmd test carrots
Python files moved to build folder [carrots.py]
0: tests/carrots/carrots.01.in
=== Diff start ===
- 1
+
=== Stop ===
   Nope

1: tests/carrots/carrots.02.in
=== Diff start ===
- 5
+
=== Stop ===
   Nope
```

First `kattcmd` moved our "solution" to the build folder. Then it ran
against `carrots.01.in` and compared it to `carrots.01.ans` and it
found that we were missing a `1` in our output. It then did the same
for the second sample test.

If you have not read the carrots problem I recommend you to do so. It
is a very easy problem to solve and showcases why it is important to
read the finer print. After you have found the solution you should
edit `kattis/carrots/carrots.py` so that it prints the solution.

Hint: It can easily be solved with 1-2 lines


# Solving and Submitting

Once you are done implementing the solution we should test it again.

```
[~/kattis] $ kattcmd test carrots
Python files moved to build folder [carrots.py]
0: tests/carrots/carrots.01.in
   OK

1: tests/carrots/carrots.02.in
   OK
```

Now that we have what seems like a solution we want to submit it to
kattis. This is easily done with `kattcmd submit`. Beware that it will
automatically open a page to your solution (or the login page for
kattis), so don't get startled by that.

```
[~/kattis] $ kattcmd submit carrots
Successful submit!
Kattis says: "Submission received. Submission ID: 2658098."
```

After that you should hopefully see that your solution made it passed
all the test cases and got accepted. Congratulations, you have solved
your first problem with the help of `kattcmd`, hope that you enjoyed
it! Feel free to read the rest of the tutorials, they may contain
useful information that help you speed up your problem solving
capabilities! Otherwise you can look at the individual commands on the
command line and see what they do with the `--help` flag. So for
example `kattcmd tips --help` will print info for the `tips` command.
