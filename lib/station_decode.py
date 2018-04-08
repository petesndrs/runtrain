'''Module station_decode
'''

from html.parser import HTMLParser


class StationDecode(HTMLParser):
    '''Class StationDecode
    '''
    td_count = 0
    station = {}
    station_list = []
    add_amp = False

    def open(self, filename):
        '''Method open
        '''
        with open(filename, 'r') as myfile:
            data = myfile.read().replace('\n', '')
        self.feed(data)

    def handle_starttag(self, tag, attrs):
        '''Method handle_starttag
        '''
        # print("Encountered a start tag:", tag)
        if tag == 'tr':
            self.td_count = 0
            self.station.clear()
        elif tag == 'td':
            self.td_count = self.td_count + 1
            # print("td_count {}".format(self.td_count))

    def handle_endtag(self, tag):
        '''Method handle_endtag
        '''
        # print("Encountered an end tag :", tag)
        if tag == 'tr':
            self.td_count = 0
            self.station.clear()

    def handle_data(self, data):
        '''Method handle_data
        '''
        # print('Data  @ td {}:{}'.format(self.td_count,data))
        if self.td_count == 1:
            if self.add_amp:
                self.station['name'] += '&{}'.format(data)
            else:
                self.station['name'] = data
        elif self.td_count == 7:
            try:
                self.station['lo'] = float(data)
            except ValueError:
                print("WARNING longitude not float " + self.station['name'])
        elif self.td_count == 8:
            try:
                self.station['la'] = float(data)
                print(self.station)
                self.station_list.append(self.station.copy())
            except ValueError:
                print("WARNING latitude not float " + self.station['name'])

        if self.add_amp:
            self.add_amp = False

    def handle_entityref(self, name):
        '''Method handle_entityref
        '''
        if name == 'amp':
            self.add_amp = True

    def get_stations(self):
        '''Method get_stations
        '''
        return self.station_list
