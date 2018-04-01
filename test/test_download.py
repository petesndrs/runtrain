'''Module test_download
'''
from pathlib import Path
from lib.download import download


def test_download():
    '''Function test_download
    '''
    filename = 'test.file'
    url = 'https://opensource.org'
    download(url, filename, True, True)

    file = Path(filename)
    assert file.is_file()
    assert file.stat().st_size

    md5_file = Path(filename + '.md5')
    assert md5_file.is_file()
    assert md5_file.stat().st_size

    time_file = Path(filename + '.time')
    assert time_file.is_file()
    assert time_file.stat().st_size

    first_time = ''
    with open(filename + '.time', 'r') as myfile:
        first_time = myfile.read()

    download(url, filename, True, True)

    new_time = ''
    with open(filename + '.time', 'r') as myfile:
        new_time = myfile.read()

    assert new_time == first_time
