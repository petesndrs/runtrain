'''Module coordinates
'''
import math


def deg_to_rad(degs):
    '''Function deg_to_rad
    '''
    return math.pi * degs / 180.0


def lat_valid(lat_degs):
    '''Function lat_valid
    '''
    return lat_degs <= 90.0 and lat_degs >= -90.0


def long_valid(long_degs):
    '''Function long_valid
    '''
    return long_degs <= 180.0 and long_degs >= -180.0


class Coordinates:
    '''Class coordinates
    '''

    def __init__(self, latitude_degs, longitude_degs):
        '''Constructor
        '''
        assert lat_valid(latitude_degs)
        assert long_valid(longitude_degs)
        self.lat = deg_to_rad(latitude_degs)
        self.long = deg_to_rad(longitude_degs)

    def distance(self, lat2_degs, long2_degs):
        '''Function distance
        '''
        return math.sqrt(self.distance_squared(lat2_degs, long2_degs))

    def distance_squared(self, lat2_degs, long2_degs):
        '''Function distance_squared
        '''
        lat2 = deg_to_rad(lat2_degs)
        long2 = deg_to_rad(long2_degs)
        return self._long_distance(lat2, long2)**2 + self._lat_distance(lat2)**2

    def _average_lat(self, lat2):
        '''Method _average_lat
        '''
        return (self.lat + lat2) / 2.0

    def _diff_lat(self, lat2):
        '''Method _diff_lat
        '''
        return math.fabs(self.lat - lat2)

    def _diff_long(self, long2):
        '''Method _diff_long
        '''
        return math.fabs(self.long - long2)

    def _long_distance(self, lat2, long2):
        '''Method _lat_distance
        '''
        return math.cos(self._average_lat(lat2)) * self._diff_long(long2)

    def _lat_distance(self, lat2):
        '''Method _long_disr=tance
        '''
        return self._diff_lat(lat2)
