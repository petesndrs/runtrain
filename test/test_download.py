'''Module test_download
'''
from pathlib import Path
from lib.download import download


def test_download():
    '''Function test_download
    '''
    filename = download('http://www.google.com')
    file = Path(filename)
    assert file.is_file()
    assert file.stat().st_size
