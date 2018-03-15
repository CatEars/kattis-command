import os
import shutil
import click


def _GetBuildFolder(bus):
    '''Returns the output build folder.'''
    home = bus.call('kattcmd:find-root', bus)
    return os.path.join(home, 'build')


def _TouchOutputFolder(bus, problemname):
    '''Creates the output folder if it does not exist.'''
    build_folder = _GetBuildFolder(bus)
    output_folder = os.path.join(build_folder, problemname)

    try:
        os.mkdir(output_folder)
    except:
        pass

    return output_folder


def _GetSourceFilesWithEndings(bus, problemname, fileendings):
    '''Returns all the source files with a specific fileending.'''
    home = bus.call('kattcmd:find-root', bus)
    problem_folder = os.path.join(home, 'kattis', problemname)
    files = os.listdir(problem_folder)

    def EndsCorrectly(fname):
        return any(fname.endswith(ending) for ending in fileendings)

    return [os.path.join(problem_folder, fname)
            for fname in files if EndsCorrectly(fname)]


def _CopyAllToBuildFolder(bus, problemname, fileendings):
    '''Copies all files matching the fileendings for problemname to output folder.'''
    build_folder = _TouchOutputFolder(bus, problemname)
    items = _GetSourceFilesWithEndings(bus, problemname, fileendings)

    def CopySingleFile(path):
        base = os.path.basename(path)
        target = os.path.join(build_folder, base)
        shutil.copyfile(path, target)
        return target

    return [CopySingleFile(item) for item in items]


def _SetTarget(builddir, targetname):
    '''Sets the most recent target in a compilation.'''
    fpath = os.path.join(builddir, '.latest')
    with open(fpath, 'w') as f:
        f.write(targetname)


def CompilePython(bus, problemname):
    '''"Compiles" python for solving problem.'''
    paths = _CopyAllToBuildFolder(bus, problemname, ['.py'])
    bus.call('kattcmd:compile:python-compiled', paths)
    return paths


def CompileCpp(bus, problemname):
    '''Compiles C++ and puts it into the build folder'''
    extensions = ['.c', '.cc', '.cxx', '.cpp', '.h', '.hh', '.hxx', '.hpp']
    paths = _CopyAllToBuildFolder(bus, problemname, extensions)
    files = [os.path.basename(f) for f in paths]

    def IsCppFile(f):
        endings = ['.c', '.cc', '.cxx', '.cpp']
        return any(f.endswith(ending) for ending in endings)

    old_cwd = os.getcwd()
    new_cwd = os.path.join(_GetBuildFolder(bus), problemname) 
    os.chdir(new_cwd)

    output_binary = problemname
    input_files = ' '.join(filter(IsCppFile, files))
    compile_command = bus.call('kattcmd:compile:cpp-command', bus)
    replacements = [
        ('BINARY', output_binary),
        ('FILES', input_files)
    ]

    for pattern, replacement in replacements:
        compile_command = compile_command.replace(pattern, replacement)

    # If the binary exists already, recompile it
    if os.path.exists(output_binary):
        os.remove(output_binary)
    try:
        os.system(compile_command)
    except Exception as e:
        bus.call('kattcmd:compile:cpp-compile-failed', compile_command)
        os.chdir(old_cwd)
        return

    if os.path.exists(output_binary):
        os.chdir(old_cwd)
        # Remove unused files
        for path in paths:
            os.remove(path)
        bus.call('kattcmd:compile:cpp-compiled', output_binary)
        relative_path = os.path.join('build', problemname, output_binary)
        return relative_path
    else:
        os.chdir(old_cwd)
        bus.call('kattcmd:compile:cpp-compile-failed', compile_command, new_cwd)


def FindCppCompileCommand(bus):
    '''Returns either the user-set compile command or the default one.'''
    default_compile = 'g++ -std=c++14 -O2 -pedantic -Wall FILES -o BINARY'
    user_compile = bus.call('kattcmd:config:load-user', bus, key='cppcompile')
    return user_compile or default_compile


def Init(bus):

    def OnCppCompileFail(compile_command):
        '''Event called when c++ fails to compile.'''

    def OnCppCompiled(binary):
        '''Event called when c++ succeds in compiling.'''

    def OnPythonCompiled(paths):
        '''Event called when python is "compiled"'''

    bus.provide('kattcmd:compile:cpp-compiled', OnCppCompiled)
    bus.provide('kattcmd:compile:cpp-compile-failed', OnCppCompileFail)
    bus.provide('kattcmd:compile:python-compiled', OnPythonCompiled)

    bus.provide('kattcmd:compile:cpp', CompileCpp)
    bus.provide('kattcmd:compile:python', CompilePython)
    bus.provide('kattcmd:compile:cpp-command', FindCppCompileCommand)


def CLI(bus, parent):

    def OnCppCompiled(binary):
        click.echo('Placed binary at {}'.format(binary))

    def OnCppCompileFailed(compile_command, directory):
        directory = os.path.relpath(directory)
        click.secho('Could not compile with "{}" in {}'.format(compile_command, directory), fg='red')
        click.echo('Exiting')
        exit(1)

    def OnPythonCompiled(paths):
        paths = list(map(os.path.relpath, paths))
        click.echo('Copied to following paths {}'.format(paths))

    def OnNoFiles(problemname):
        click.secho('Could not find any "compilable" items for "{}"'.format(problemname), fg='red')
        click.echo('Exiting')
        exit(1)

    @parent.command()
    @click.argument('name')
    def compile(name):
        '''Compile your solution to a problem.

        Will compile your solution and put it inside the build
        folder. If you use an interpreted language then it will copy
        it instead.

        This command is useful if you want to run the code yourself
        against some specific input.

        '''
        bus.listen('kattcmd:compile:cpp-compiled', OnCppCompiled)
        bus.listen('kattcmd:compile:cpp-compile-failed', OnCppCompileFailed)
        bus.listen('kattcmd:compile:python-compiled', OnPythonCompiled)
        bus.listen('kattcmd:latest:no-files', OnNoFiles)

        value = bus.call('kattcmd:latest', bus, name)
        if not value:
            click.secho('Could not determine what you worked on previously', fg='red')
            click.echo('Exiting')
            return None

        type, _ = value
        if type == 'python':
            bus.call('kattcmd:compile:python', bus, name)
        elif type == 'cpp':
            bus.call('kattcmd:compile:cpp', bus, name)
        else:
            raise ValueError('{} is not an implemented type'.format(type))
