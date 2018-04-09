'''Module parkrun_events
'''
import argparse
import logging
import fileinput
import re
import semver

from lib.time_string import time_string
from lib.download import download
from lib.geo_decode import GeoDecode
from lib.station_decode import StationDecode
from lib.code_decode import CodeDecode
from lib.git_interface import git_sha, git_branch
from lib.coordinates import Coordinates

MAJOR = 0
MINOR = 1
PATCH = 0

URL = 'https://www.parkrun.org.uk/wp-content/themes/parkrun/xml/geo.xml'

STATION_BASE_URL = 'http://www.railwaycodes.org.uk/stations/'
STATION_PAGES = ['stationa.shtm', 'stationb.shtm',
                 'stationc.shtm', 'stationd.shtm',
                 'statione.shtm', 'stationf.shtm',
                 'stationg.shtm', 'stationh.shtm',
                 'stationi.shtm', 'stationj.shtm',
                 'stationk.shtm', 'stationl.shtm',
                 'stationm.shtm', 'stationn.shtm',
                 'stationo.shtm', 'stationp.shtm',
                 'stationq.shtm', 'stationr.shtm',
                 'stations.shtm', 'stationt.shtm',
                 'stationu.shtm', 'stationv.shtm',
                 'stationw.shtm', 'stationy.shtm']

STATION_CODES_URL = 'http://www.nationalrail.co.uk/static/' + \
                    'documents/content/station_codes.csv'


EVENT_FORMAT = '        {{ name:"{}", link:"{}", lo:"{}", la:"{}", ' + \
               'station:"{}", slo:"{}", sla:"{}"}},\n'


# pylint: disable=too-many-branches
# pylint: disable=too-many-return-statements
def name_match(name1, name2, strength):
    '''Function name_match
    '''
    name1_no_punc = re.sub('[!@#$."\']', '', name1)
    name2_no_punc = re.sub('[!@#$."\']', '', name2)
    name1_lower = name1_no_punc.lower()
    name2_lower = name2_no_punc.lower()
    if strength == 1:
        if name1_lower == name2_lower:
            return 1
        return 0

    name1_hyphenless = name1_lower.replace('-', ' ')
    name2_hyphenless = name2_lower.replace('-', ' ')
    if strength == 2:
        if name1_hyphenless == name2_hyphenless:
            return 2
        return 0

    if strength == 3:
        if ('(' in name1_hyphenless and
                ')' in name1_hyphenless and
                '(' in name2_hyphenless and
                ')' in name2_hyphenless):
            counties = [
                {'long': 'bedfordshire', 'short': 'beds'},
                {'long': 'berkshire', 'short': 'berks'},
                {'long': 'cambridgeshire', 'short': 'cambs'},
                {'long': 'greater london', 'short': 'london'},
                {'long': 'hampshire', 'short': 'hants'},
                {'long': 'hertfordshire', 'short': 'herts'},
                {'long': 'lanarkshire', 'short': 'lanark'},
                {'long': 'lancashire', 'short': 'lancs'},
                {'long': 'leicestershire', 'short': 'leics'},
                {'long': 'lincolnshire', 'short': 'lincs'},
                {'long': 'greater manchester', 'short': 'manchester'},
                {'long': 'oxfordshire', 'short': 'oxon'},
                {'long': 'pembrokeshire', 'short': 'pembs'},
                {'long': 'staffordshire', 'short': 'staffs'},
                {'long': 'warwickshire', 'short': 'warks'},
                {'long': 'wiltshire', 'short': 'wilts'},
                {'long': 'yorkshire', 'short': 'yorks'}
            ]

            for county in counties:
                name1_shortened = name1_hyphenless.replace(county['long'], county['short'])
                name2_shortened = name2_hyphenless.replace(county['long'], county['short'])
                if name1_shortened == name2_shortened:
                    print('MAGIC {} == {}'.format(name1_hyphenless, name2_hyphenless))
                    return 3
        return 0

    if strength == 4:
        if '(' in name1_hyphenless:
            if name1_hyphenless.replace('(', '').replace(')', '') == name2_hyphenless:
                print('MAGIC A {} == {}'.format(name1_hyphenless, name2_hyphenless))
                return 4
        elif '(' in name2_hyphenless:
            if name1_hyphenless == name2_hyphenless.replace('(', '').replace(')', ''):
                print('MAGIC B {} == {}'.format(name1_hyphenless, name2_hyphenless))
                return 4
        return 0

    if strength == 5:
        if '(' in name1_hyphenless and '(' in name2_hyphenless:
            if name1_hyphenless.split('(')[0] == name2_hyphenless.split('(')[0]:
                print('MAGIC1 {} == {}'.format(name1_hyphenless, name2_hyphenless))
                return 5
        elif '(' in name1_hyphenless:
            if name1_hyphenless.split('(')[0][:-1] == name2_hyphenless:
                print('MAGIC2 {} == {}'.format(name1_hyphenless, name2_hyphenless))
                return 5
        elif '(' in name2_hyphenless:
            if name1_hyphenless == name2_hyphenless.split('(')[0][:-1]:
                print('MAGIC3 {} == {}'.format(name1_hyphenless, name2_hyphenless))
                return 5
        return 0

    if strength == 6:
        if name1_hyphenless.split(' ')[0] == name2_hyphenless.split(' ')[0]:
            print('FORCED {} == {}'.format(name1_hyphenless, name2_hyphenless))
            return 6
        return 0
    return 0


# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=too-many-nested-blocks
def main():
    '''Function main
    '''
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--update', help='Update event information',
                        action='store_true')
    parser.add_argument('-s', '--station', help='Update station information',
                        action='store_true')
    cmd_line_args = parser.parse_args()

    filename = 'data/geo.xml'
    if cmd_line_args.update:
        filename = 'geo.xml'
        download(URL, filename, True, True)

    logging.info("Using data file %s", filename)

    geo_decoder = GeoDecode(filename)
    regions = geo_decoder.get_regions()
    events = geo_decoder.get_events()
    print(regions)
    print(events)

    if cmd_line_args.station:
        download(STATION_CODES_URL, 'data/station_codes.csv', True, True)
        for page in STATION_PAGES:
            download(STATION_BASE_URL + page, 'data/' + page, True, True)

    parser = StationDecode()
    for page in STATION_PAGES:
        parser.open('data/' + page)
    stns = parser.get_stations()
    print(stns)

    code_parser = CodeDecode('data/station_codes.csv')
    codes = code_parser.get_codes()

    # append station geographical info to code data
    total = len(codes)
    print('Total = {}'.format(total))
    for strength in range(1, 7):
        print('Strength = {}'.format(strength))
        matches = 0
        for code in codes:
            if 'station' not in code:
                found_station = None
                finds = 0
                for station in stns:
                    if 'used' not in station:
                        # full match
                        match_type = name_match(code['name'], station['name'], strength)
                        if match_type:
                            finds += 1
                            found_station = station

                if finds > 1:
                    print('Dodgy? {} <-> {}'.format(code['name'], found_station['name']))
                elif finds == 1:
                    matches += 1
                    code['station'] = found_station
                    found_station['used'] = 1

        print('Matches at this strength = {} ({}%)'.format(matches, 100.0 * matches / total))

    for code in codes:
        if 'station' not in code:
            print("WARNING: Cannot find {}({}) in stations".format(code['name'], code['code']))

    for event in events:
        closest_dist = 1000.0
        closest_station = {}
        event_coord = Coordinates(event['la'], event['lo'])
        for code in codes:
            # may not have a station for every code
            if 'station' in code:
                dist = event_coord.distance(code['station']['la'], code['station']['lo'])
                if dist < closest_dist:
                    closest_dist = dist
                    closest_station = code
        event['code'] = closest_station
        print(event['n'] + ' ' + event['code']['name'])

    outfile = open("docs/runtrain.html", 'w')
    for line in fileinput.FileInput("runtrain.template.html"):
        outfile.write(line)
        if "INSERT-REGIONS-HERE" in line:
            print(line)
            for region in regions:
                outfile.write('    {{ name:"{}", id:{} }},\n'.format(region['n'], region['id']))
        if "INSERT-EVENTS-HERE" in line:
            print(line)
            for region in regions:
                outfile.write('    {{ region:{}, event_list:[\n'.format(region['id']))
                for event in events:
                    if event['r'] == region['id']:
                        outfile.write(EVENT_FORMAT.
                                      format(event['m'], event['n'],
                                             event['lo'], event['la'],
                                             event['code']['station']['name'],
                                             event['code']['station']['lo'],
                                             event['code']['station']['la']))
                outfile.write('        ]},\n')
        if "INSERT-DATE-HERE" in line:
            time = time_string()
            outfile.write('    "{}"+\n'.format(time))
        if "INSERT-VERSION-HERE" in line:
            version = semver.format_version(MAJOR, MINOR, PATCH, git_branch(), git_sha())
            print(version)
            outfile.write('    "{}"+\n'.format(version))


if __name__ == "__main__":
    main()
