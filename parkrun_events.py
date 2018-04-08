'''Module parkrun_events
'''
import argparse
import logging
import fileinput
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
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
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
    full_match = 0
    partial_match = 0
    total = 0
    for code in codes:
        found_station = None
        total += 1
        for station in stns:
            # full match
            if station['name'].lower() == code['name'].lower():
                full_match += 1
                found_station = station

        if not found_station:
            finds = 0
            candidate_station = None
            for station in stns:
                if station['name'].lower().find(code['name'].lower()) == 0:
                    # print('code-name {} in station-name {}'.format(code['name'],station['name']))
                    candidate_station = station
                    finds += 1
                if code['name'].lower().find(station['name'].lower()) == 0:
                    # print('station-name {} in code-name {}'.format(station['name'],code['name']))
                    candidate_station = station
                    finds += 1
            if finds == 1:
                partial_match += 1
                found_station = candidate_station
                print('WARNING: Matching {} to {}'.format(code['name'], found_station['name']))

        if found_station:
            code['station'] = found_station
        else:
            print("WARNING: Cannot find {}({}) in stations".format(code['name'], code['code']))
    # print(codes)
    print('Full Match: {} ({}%)'.format(full_match, 100.0 * full_match / total))
    print('Part Match: {} ({}%)'.format(partial_match, 100.0 * partial_match / total))
    print('All  Match: {} ({}%)'.format(full_match + partial_match,
                                        100.0 * (full_match + partial_match) / total))
    print('Total     : {}'.format(total))

    for event in events:
        closest_dist = 1000.0
        closest_station = {}
        event_coord = Coordinates(event['la'], event['lo'])
        for station in stns:
            dist = event_coord.distance(station['la'], station['lo'])
            if dist < closest_dist:
                closest_dist = dist
                closest_station = station
        event['station'] = closest_station
        print(event['n'] + ' ' + event['station']['name'])

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
                                             event['station']['name'],
                                             event['station']['lo'],
                                             event['station']['la']))
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
