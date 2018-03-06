import os
import requests
import zipfile
import io

def _GetProblemZip(problemname):
    url = 'https://open.kattis.com/problems/'
    path = '{}/file/statement/samples.zip'.format(problemname)
    return url + path


def _TouchDir(directory):
    try:
        os.mkdir(directory)
    except FileExistsError:
        pass


def DownloadTest(bus, problemname):
    '''Download tests and puts them into the right folder.'''
    # Download the tests for problemname and put them inside correct
    # testfolder. If it doesn't exist, create it.
    the_url = _GetProblemZip(problemname)
    root = bus.call('kattcmd:find-root', bus)
    test_dir = os.path.join(root, 'tests', problemname)
    _TouchDir(test_dir)

    response = requests.get(the_url)
    if response.status_code == 200:
        buffer_view = io.BytesIO(response.content)
        z = zipfile.ZipFile(buffer_view)
        z.extractall(test_dir)
        bus.call('kattcmd:testdownload:downloaded', test_dir)

    else:
        bus.call('kattcmd:testdownload:bad-status', response)


def Init(bus):

    def on_download(directory):
        '''Event called when a problem was downloaded.'''

    def on_bad_status(response):
        '''Event called when a problem could not be downloaded.'''

    bus.provide('kattcmd:testdownload', DownloadTest)
    bus.provide('kattcmd:testdownload:downloaded', on_download)
    bus.provide('kattcmd:testdownload:bad-status', on_bad_status)
