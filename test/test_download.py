'''Module test_download
'''
from pathlib import Path
from lib.download import download


def test_download():
    '''Function test_download
    '''
    filename = 'test.file'
    download('http://www.google.com', filename)
    file = Path(filename)
    assert file.is_file()
    assert file.stat().st_size
