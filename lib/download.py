'''Module download
'''
import wget


def download(url):
    '''Function download
    '''
    filename = wget.download(url)
    return filename
