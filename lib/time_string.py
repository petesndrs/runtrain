'''Module download
'''
from datetime import datetime

DATE_DIGITS = 10
DATE_HOUR_DIGITS = 14
DATE_HOUR_MIN_DIGITS = 17
DATE_HOUR_MIN_SEC_DIGITS = 19

TIME_STRING_REGEX = '^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$'


def time_string():
    '''Function time_string
    '''
    return str(datetime.utcnow()).split('.')[0]
