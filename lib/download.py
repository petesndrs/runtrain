'''Module download
'''
import requests


def download(url, fname):
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
