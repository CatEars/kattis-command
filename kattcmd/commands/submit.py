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

    def __init__(self, message):
        self.message = message


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
        raise LoginError('No .kattisrc file present. Make sure to download it')
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


def SubmitCppProblem(bus, problemname):
    '''Submits a cpp problem to kattis.'''

    response = _Login(bus)
    if response.status_code != 200:
        bus.call('kattcmd:submit:bad-login-response', response)
        return

    extensions = ['.cc', '.cpp', '.cxx', '.h', '.hh', '.hpp', '.hxx']
    files = _GetFilesWithExtensions(bus, problemname, extensions)
    language = 'C++'
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
    bus.provide('kattcmd:submit:cpp', SubmitCppProblem)


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

        pattern = r'\d+' # Finds a number
        ids = re.findall(pattern, response.text)
        if not ids:
            return # Could not find submission ID
        config = _GetUserConfig(bus)
        url = urllib.parse.urlparse(config.get('kattis', 'loginurl'))
        host = url.scheme + '://' + url.hostname
        problemurl = '{}/submissions/{}'.format(host, ids[0])
        click.launch(problemurl)

    def OnNoFiles(problemname):
        click.secho('Could not find any files for "{}"!'.format(problemname), fg='red')
        click.echo('Exiting')
        exit(1)

    @parent.command()
    @click.argument('name')
    def submit(name):
        '''Submits a problem to kattis.

        When you have implemented and tested a problem this command
        will upload it to kattis and then open the submission in your
        browser. It will look for the files you modified most recently
        and use the language that is written in to determine what to
        files to upload.

        '''
        bus.listen('kattcmd:submit:bad-login-response', OnBadLoginResponse)
        bus.listen('kattcmd:submit:bad-submit-response', OnBadSubmitResponse)
        bus.listen('kattcmd:submit:submitted', OnSubmitted)
        bus.listen('kattcmd:latest:no-files', OnNoFiles)

        language, _ = bus.call('kattcmd:latest', bus, name)
        if language == 'python':
            bus.call('kattcmd:submit:python', bus, name)
        elif language == 'cpp':
            bus.call('kattcmd:submit:cpp', bus, name)
        else:
            click.secho('Unsupported language!', fg='red')
