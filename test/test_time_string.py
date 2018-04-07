'''Module test_time_string
'''
import time
import re
from datetime import datetime

from lib.time_string import time_string, TIME_STRING_REGEX,\
    DATE_DIGITS, DATE_HOUR_DIGITS, DATE_HOUR_MIN_DIGITS

EARLIER = '2018-01-01 17:30:00'
LATER = '2118-01-01 17:30:00'


def test_time_string():
    '''Function test_time_string
    '''
    date1 = datetime.utcnow()
    string1 = time_string()
    time.sleep(2)
    string2 = time_string()
    date2 = datetime.utcnow()

    # Check both part of regex
    assert re.fullmatch(TIME_STRING_REGEX, string1)
    assert re.fullmatch(TIME_STRING_REGEX, string2)

    # Check second is later
    assert string2 > string1

    if date1.date() == date2.date():
        assert string1[1:DATE_DIGITS] == string2[1:DATE_DIGITS]
    if date1.time().hour == date2.time().hour:
        assert string1[1:DATE_HOUR_DIGITS] == string2[1:DATE_HOUR_DIGITS]
    if date1.time().minute == date2.time().minute:
        assert string1[1:DATE_HOUR_MIN_DIGITS] == string2[1:DATE_HOUR_MIN_DIGITS]

    assert string1 > EARLIER
    assert LATER > string2
