'''Module geo_decode
'''

import xml.etree.ElementTree as ET


class GeoDecode:
    '''Class geo_decode
    '''

    def __init__(self, filename):
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()
        self.events = []
        self.regions = []
        self.regions_ids = []
        self.decode_regions_uk()
        self.decode_events_uk()

    def decode_events_uk(self):
        '''Method decode_events_uk
        '''
        self.decode_events('97')

    def decode_events(self, country_code):
        '''Method decode_events
        '''
        for child in self.root:
            # print(child.tag)
            # print(child.attrib)
            if child.tag == 'e' and child.attrib['c'] == country_code:
                # replace unicode characters that can't be converted to strings
                child.attrib['m'] = child.attrib['m'].\
                    replace(u"\u2018", "'").\
                    replace(u"\u2019", "'")
                print(child.attrib['m'],
                      child.attrib['la'],
                      child.attrib['lo'], child.attrib['r'])

                try:
                    child.attrib['lo'] = float(child.attrib['lo'])
                    child.attrib['la'] = float(child.attrib['la'])
                except ValueError:
                    print("WARNING latitude/longitude not float " + child.attrib['m'])

                if child.attrib['r'] not in self.regions_ids:
                    print('WARNING: ')
                    print(child.attrib)
                else:
                    self.events.append(child.attrib)

    def decode_regions_uk(self):
        '''Method decode_regions_uk
        '''
        self.decode_regions('2')

    def decode_regions(self, country_region):
        '''Method decode_regions
        '''
        for child in self.root:
            if child.tag == 'r':
                # print (child.attrib)
                for country in child:
                    # print (country.attrib)
                    if country.attrib['id'] == country_region:
                        for region in country:
                            print(region.attrib['n'], region.attrib['id'])
                            self.regions.append(region.attrib)
                            self.regions_ids.append(region.attrib['id'])

    def get_regions(self):
        '''Method regions
        '''
        return self.regions

    def get_events(self):
        '''Method events
        '''
        return self.events
