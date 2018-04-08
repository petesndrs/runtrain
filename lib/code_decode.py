'''Module code_decode
'''


# pylint: disable=too-few-public-methods
class CodeDecode():
    '''Class CodeDecode
    '''
    codes = []

    def __init__(self, filename):
        '''Constructor
        '''
        with open(filename, 'r') as myfile:
            lines = myfile.readlines()

        for line in lines:
            # print(line)
            itemlist = []
            itemlist = line.split(',')
            station = {}
            station['name'] = itemlist[0].strip()
            station['code'] = itemlist[-1].strip()
            if len(station['code']) == 3:
                self.codes.append(station)
        print(self.codes)

    def get_codes(self):
        '''Method get_codes
        '''
        return self.codes
