'''Module test_geo_decode
'''

from lib.geo_decode import GeoDecode


def test_download():
    '''Function test_download
    '''
    filename = 'test/test_geo.xml'
    geo_decoder = GeoDecode(filename)
    regions = geo_decoder.get_regions()
    events = geo_decoder.get_events()
    assert len(regions) == 13
    assert len(events) == 517
