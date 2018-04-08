'''Module test_code_decode
'''

from lib.code_decode import CodeDecode


def test_decode():
    '''Function test_decode
    '''
    filename = 'test/test_codes.csv'
    code_decoder = CodeDecode(filename)
    codes = code_decoder.get_codes()
    assert len(codes) == 2570
