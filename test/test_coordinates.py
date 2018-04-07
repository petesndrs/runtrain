'''Module test_coordinates
'''
import math

from lib.coordinates import deg_to_rad
from lib.coordinates import Coordinates

TOLERANCE_RADS = 0.01

TOLERANCE_LINEAR = 0.01


def test_deg_to_rad():
    '''Function test_deg_to_rad
    '''
    assert deg_to_rad(0.0) < TOLERANCE_RADS
    assert deg_to_rad(180.0) > (math.pi - TOLERANCE_RADS)
    assert deg_to_rad(180.0) < (math.pi + TOLERANCE_RADS)
    assert deg_to_rad(360.0) > (2.0 * math.pi - TOLERANCE_RADS)
    assert deg_to_rad(360.0) < (2.0 * math.pi + TOLERANCE_RADS)


def test_distance_same_lat():
    '''Function test_distance_same_lat():
    '''
    coord1 = Coordinates(0.0, 0.0)
    assert coord1.distance(0.0, 0.0) < TOLERANCE_LINEAR
    assert coord1.distance(0.0, 90.0) > ((math.pi / 2.0) - TOLERANCE_LINEAR)
    assert coord1.distance(0.0, 90.0) < ((math.pi / 2.0) + TOLERANCE_LINEAR)
    assert coord1.distance(0.0, -90.0) > ((math.pi / 2.0) - TOLERANCE_LINEAR)
    assert coord1.distance(0.0, -90.0) < ((math.pi / 2.0) + TOLERANCE_LINEAR)

    coord2 = Coordinates(0.0, 45.0)
    assert coord2.distance(0.0, -45.0) > ((math.pi / 2.0) - TOLERANCE_LINEAR)
    assert coord2.distance(0.0, -45.0) < ((math.pi / 2.0) + TOLERANCE_LINEAR)

    coord3 = Coordinates(0.0, 90.0)
    assert coord3.distance(0.0, -90.0) > (math.pi - TOLERANCE_LINEAR)
    assert coord3.distance(0.0, -90.0) < (math.pi + TOLERANCE_LINEAR)


def test_distance_same_long():
    '''Function test_distance_same_long():
    '''
    coord1 = Coordinates(0.0, 0.0)
    assert coord1.distance(0.0, 0.0) < TOLERANCE_LINEAR
    assert coord1.distance(90.0, 0.0) > ((math.pi / 2.0) - TOLERANCE_LINEAR)
    assert coord1.distance(90.0, 0.0) < ((math.pi / 2.0) + TOLERANCE_LINEAR)
    assert coord1.distance(-90.0, 0.0) > ((math.pi / 2.0) - TOLERANCE_LINEAR)
    assert coord1.distance(-90.0, 0.0) < ((math.pi / 2.0) + TOLERANCE_LINEAR)
    assert coord1.distance(180.0, 0.0) > (math.pi - TOLERANCE_LINEAR)
    assert coord1.distance(180.0, 0.0) < (math.pi + TOLERANCE_LINEAR)
    assert coord1.distance(-180.0, 0.0) > (math.pi - TOLERANCE_LINEAR)
    assert coord1.distance(-180.0, 0.0) < (math.pi + TOLERANCE_LINEAR)

    coord2 = Coordinates(90.0, 0.0)
    assert coord2.distance(-90.0, 0.0) > (math.pi - TOLERANCE_LINEAR)
    assert coord2.distance(-90.0, 0.0) < (math.pi + TOLERANCE_LINEAR)

    coord3 = Coordinates(45.0, 0.0)
    assert coord3.distance(-45.0, 0.0) > ((math.pi / 2.0) - TOLERANCE_LINEAR)
    assert coord3.distance(-45.0, 0.0) < ((math.pi / 2.0) + TOLERANCE_LINEAR)
