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
from lib.git_interface import git_sha, git_branch

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


# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
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
        for page in STATION_PAGES:
            download(STATION_BASE_URL + page, 'data/' + page, True, True)

    parser = StationDecode()
    for page in STATION_PAGES:
        parser.open('data/' + page)
    stns = parser.get_stations()
    print(stns)

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
                        outfile.write('        {{ name:"{}", link:"{}", lo:"{}", la:"{}"}},\n'.
                                      format(event['m'], event['n'], event['lo'], event['la']))
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
