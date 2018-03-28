'''Module parkrun_events
'''
from datetime import datetime
import fileinput
import xml.etree.ElementTree as ET

from lib.download import download

URL = 'https://www.parkrun.org.uk/wp-content/themes/parkrun/xml/geo.xml'


# pylint: disable=too-many-branches
def main():
    '''Function main
    '''
    filename = download(URL)
    print(filename)

    tree = ET.parse(filename)
    root = tree.getroot()

    events = []
    regions = []
    regions_ids = []

    for child in root:
        # print(child.tag)
        # print(child.attrib)
        if child.tag == 'e' and child.attrib['c'] == '97':
            # replace unicode characters that can't be converted to strings
            child.attrib['m'] = child.attrib['m'].replace(u"\u2018", "'").replace(u"\u2019", "'")
            print(child.attrib['m'],
                  child.attrib['la'],
                  child.attrib['lo'], child.attrib['r'])
            if child.attrib['r'] not in regions_ids:
                print('WARNING: ')
                print(child.attrib)
            else:
                events.append(child.attrib)
        elif child.tag == 'r':
            # print (child.attrib)
            for country in child:
                # print (country.attrib)
                if country.attrib['id'] == '2':
                    for region in country:
                        print(region.attrib['n'], region.attrib['id'])
                        regions.append(region.attrib)
                        regions_ids.append(region.attrib['id'])

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


if __name__ == "__main__":
    main()
