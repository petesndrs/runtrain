'''Module download
'''
import hashlib
from pathlib import Path
import requests
from lib.time_string import time_string


def download(url, fname, add_md5, add_time):
    '''Function download
    '''
    fake_headers = requests.utils.default_headers()

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) ' +\
        'AppleWebKit/537.36 (KHTML, like Gecko) ' +\
        'Chrome/64.0.3282.186 Safari/537.36 OPR/51.0.2830.55'

    fake_headers.update({'User-Agent': user_agent})

    response = requests.get(url, headers=fake_headers)
    with open(fname, 'wb')as file_handle:
        file_handle.write(response.content)

    old_md5 = ''
    if Path(fname + '.md5').is_file():
        with open(fname + '.md5', 'r') as myfile:
            old_md5 = myfile.read()

    new_md5 = hashlib.md5(response.content).hexdigest()
    if add_md5:
        if old_md5 != new_md5:
            with open(fname + '.md5', 'w') as outfile:
                outfile.write(new_md5)
            if add_time:
                with open(fname + '.time', 'w') as outfile:
                    outfile.write(time_string())
