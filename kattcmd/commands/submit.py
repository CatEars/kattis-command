import click
import configparser
import os
import re
import requests
import urllib.parse

HEADERS = {
    'User-Agent': 'kattcmd-cli-utility'
}

class LoginError(Exception):
    pass


def _GetFilesWithExtensions(bus, problemname, exts):
    '''Returns all files for the problem matching the given extensions.'''

    def MatchesExt(fpath):
        return any(fpath.endswith(ext) for ext in exts)

    home = bus.call('kattcmd:find-root', bus)
    problemfolder = os.path.join(home, 'kattis', problemname)
    items = [os.path.join(problemfolder, item) for item in os.listdir(problemfolder)]
    return list(filter(MatchesExt, items))


def _GetUserConfig(bus):
    configfile = bus.call('kattcmd:config:load-user', bus, 'kattisrc')
    if not configfile or not os.path.isfile(configfile):
        raise LoginError('No .kattisrc file present')
    config = configparser.ConfigParser()
    config.read(configfile)
    return config


def _Login(bus):
    '''Logs into kattis and returns the response. Quits on bad status.'''
    config = _GetUserConfig(bus)
    username = config.get('user', 'username')
    token = config.get('user', 'token')
    data = {
        'user': username,
        'script': 'true',
        'token': token
    }

    loginurl = config.get('kattis', 'loginurl')
    return requests.post(loginurl, data=data, headers=HEADERS)


def _Submit(submiturl, cookies, language, problemname, files, mainclass):

    def ReadData(fpath):
        with open(fpath, 'rb') as f:
            return f.read()

    def ConvertFile(fpath):
        return (
            "sub_file[]",
            (
                os.path.basename(fpath),
                ReadData(fpath),
                'application/octet-stream'
            )
        )

    files_to_be_sent = list(map(ConvertFile, files))
    data = {
        'submit': 'true',
        'language': language,
        'submit_ctr': 2, # Apparently this is necessary (?)
        'mainclass': mainclass,
        'problem': problemname,
        'script': 'true'
    }

    return requests.post(submiturl, files=files_to_be_sent, data=data,
                         cookies=cookies, headers=HEADERS)

def SubmitPythonProblem(bus, problemname):
    '''Submits a python problem to kattis.'''

    # Try to login and if that doesn't work then jump out.
    response = _Login(bus)
    if response.status_code != 200:
        bus.call('kattcmd:submit:bad-login-response', response)
        return

    files = _GetFilesWithExtensions(bus, problemname, ['.py'])
    language = 'Python 3'
    submiturl = _GetUserConfig(bus).get('kattis', 'submissionurl')
    submit_response = _Submit(submiturl, response.cookies, language,
                       problemname, files, problemname)

    if submit_response.status_code != 200:
        bus.call('kattcmd:submit:bad-submit-response', submit_response)
        return

    bus.call('kattcmd:submit:submitted', submit_response)
    return submit_response

def Init(bus):

    def OnBadLoginResponse(response):
        '''Event called when login was unsuccessfull.'''

    def OnBadSubmitResponse(response):
        '''Event called when submission was unsuccessfull.'''

    def OnSubmitted(response):
        '''Event called when a submission was successfull.'''

    bus.provide('kattcmd:submit:python', SubmitPythonProblem)
    bus.provide('kattcmd:submit:bad-login-response', OnBadLoginResponse)
    bus.provide('kattcmd:submit:bad-submit-response', OnBadSubmitResponse)
    bus.provide('kattcmd:submit:submitted', OnSubmitted)


def CLI(bus, parent):

    def OnBadLoginResponse(response):
        click.secho('Error during login:', fg='red', bold=True)
        click.echo(str(response))

    def OnBadSubmitResponse(response):
        click.secho('Error during submit:', fg='red', bold=True)
        click.echo(str(response))

    def OnSubmitted(response):
        click.secho('Successful submit!', fg='green', bold=True)
        click.echo('Kattis says: "{}"'.format(response.text))

        pattern = r'\d+'
        ids = re.findall(pattern, response.text)
        if not ids:
            return # Could not find submission ID
        config = _GetUserConfig(bus)
        url = urllib.parse.urlparse(config.get('kattis', 'loginurl'))
        host = url.scheme + '://' + url.hostname
        problemurl = '{}/submissions/{}'.format(host, ids[0])
        click.launch(problemurl)

    @parent.command()
    @click.argument('name')
    @click.argument('language', default='python', type=click.Choice(['python', 'cpp']))
    def submit(name, language):
        bus.listen('kattcmd:submit:bad-login-response', OnBadLoginResponse)
        bus.listen('kattcmd:submit:bad-submit-response', OnBadSubmitResponse)
        bus.listen('kattcmd:submit:submitted', OnSubmitted)

        if language == 'python':
            bus.call('kattcmd:submit:python', bus, name)
        else:
            click.secho('Unsupported language!', fg='red')
