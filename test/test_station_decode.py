'''Module test_station_decode
'''

from lib.station_decode import StationDecode


def test_station():
    '''Function test_station
    '''
    parser = StationDecode()
    parser.feed('<tr>'
                '<td></td><td>ABC</td><td></td>'
                '<td></td><td></td><td></td>'
                '<td>11</td><td>22</td><td></td>'
                '</tr>')
    station_list = parser.get_stations()
    assert len(station_list) == 1
