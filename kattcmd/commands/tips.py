import click


def Init(bus):
    pass


def CLI(bus, parent):

    @parent.command()
    def tips():
        '''General usage tips.'''
        click.clear()
        click.echo('kattcmd is built in such a way that is highly configurable.')
        click.echo('Therefore it is important for your enjoyment with the tool that you ' + \
                   'configure it well, which we will do now!')
        click.pause()

        click.echo('')
        click.secho('=== .kattisrc ===', fg='blue')
        click.echo('The first thing that you want to do is make sure that you have downloaded ' + \
                   'the .kattisrc from the kattis you want to work with.')
        click.echo('For example if you are working on open.kattis.com you want to head over ' + \
                   'to https://open.kattis.com/download/kattisrc and follow the ' + \
                   'instructions there.')
        do = click.confirm('Do you want me to take you to your kattisrc now ? (login required) ')

        if do:
            click.echo('Okay, what kattis is it? Examples: "open", "liu", "iceland", "kth"')
            domain = click.prompt('Enter your domain: ', type=str).strip()
            url = 'https://{}.kattis.com/download/kattisrc'.format(domain)
            click.launch(url)

        click.echo('The .kattisrc should be put as ~/.kattisrc')
        click.pause('Press enter to continue once you have made sure you have a .kattisrc...')

        click.echo('Great! Lets get going configuring your kattcmd setup.')

        # Get user information
        click.echo('')
        click.secho('=== User Info ===', fg='blue')
        click.echo('When opening new problems, kattcmd will automatically move a template ' + \
                   'into your solution folder.')
        click.echo('By default it uses python but you can specify what you want to use from: [python, C++]')
        do = click.confirm('Do you want to change that now? ')

        if do:
            value = click.prompt('Okay, do you want "python" or "cpp"? ', type=str)
            while value.strip() not in ['python', 'cpp']:
                click.echo('You have to choose either python or cpp!')
                value = click.prompt('Okay, do you want "python" or "cpp"? ')
            bus.call('kattcmd:config:add-user', bus, 'template-type', value.strip())

        # Get name
        click.echo('')
        click.echo('kattcmd will also automatically add your name to any new problem opened.')
        click.echo('It does so by replacing "ZZZ" with your username.')
        do = click.confirm('Do you want to enter your name and have it pop up in the template?')

        if do:
            value = click.prompt('Enter your name: ', type=str).strip()
            bus.call('kattcmd:config:add-user', bus, 'name', value)

        # Get C++ command
        click.echo('')
        click.echo('If you will be using C++ then you will be using a command to compile it.')
        command = bus.call('kattcmd:compile:cpp-command', bus)
        click.echo('Right now it is: "{}"'.format(command))
        click.echo('When compiling, kattcmd will use the above command but replace FILES ' + \
                   'with the input files and BINARY with the output binary')
        dont = click.confirm('Do you want to use the above command for C++ compilation? ')

        if not dont:
            click.echo('Remember to use FILES and BINARY in your command where it is relevant!')
            value = click.prompt('Enter C++ compile command: ', type=str).strip()
            bus.call('kattcmd:config:add-user', bus, 'cppcompile', value)


