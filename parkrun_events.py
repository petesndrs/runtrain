'''Module parkrun_events
'''
import argparse
import logging
from datetime import datetime
import fileinput
import semver

from lib.download import download
from lib.geo_decode import GeoDecode
from lib.git_interface import git_sha, git_branch

MAJOR = 0
MINOR = 1
PATCH = 0

URL = 'https://www.parkrun.org.uk/wp-content/themes/parkrun/xml/geo.xml'


# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
def main():
    '''Function main
    '''
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--update', help='Update event information',
                        action='store_true')
    cmd_line_args = parser.parse_args()

    filename = 'data/geo.xml'
    if cmd_line_args.update:
        filename = 'geo.xml'
        download(URL, filename)

    logging.info("Using data file %s", filename)

    geo_decoder = GeoDecode(filename)
    regions = geo_decoder.get_regions()
    events = geo_decoder.get_events()
    print(regions)
    print(events)

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
                        outfile.write('        {{ name:"{}", link:"{}"}},\n'.
                                      format(event['m'], event['n']))
                outfile.write('        ]},\n')
        if "INSERT-DATE-HERE" in line:
            d_t = datetime.utcnow()
            outfile.write('    "{}"+\n'.format(d_t))
        if "INSERT-VERSION-HERE" in line:
            version = semver.format_version(MAJOR, MINOR, PATCH, git_branch(), git_sha())
            print(version)
            outfile.write('    "{}"+\n'.format(version))


if __name__ == "__main__":
    main()
