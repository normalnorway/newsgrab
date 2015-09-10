"""
Utilities to handle Norwegian dates.
"""

import re
from datetime import datetime, timedelta


_ISO_DATE_REGEX =  re.compile (r'(.*)(?:\.\d{3})?([+-])(\d\d):?(\d\d)?$')


def last_sunday_of_month (year, month):
    """Return day number of last sunday in the month.
       Stolen from http://stackoverflow.com/a/29338804"""
    import calendar
    obj = calendar.monthcalendar (year, month)
    return max (obj[-1][calendar.SUNDAY], obj[-2][calendar.SUNDAY])


# Note: the passed datetime object is assumed to be in zulu time!
def is_dst (dt):
    """Return true if daylight saving time is in effect (in Norway)"""
    assert (dt.year >= 1980)
    if dt.month < 3:  return False  # mars
    if dt.month > 10: return False  # oktober
    if dt.month in [3,10]:
        cutoff = dt.replace (day = last_sunday_of_month (dt.year, dt.month),
                             hour=2-1, minute=0, second=0)
        if dt.month ==  3: return dt >= cutoff
        if dt.month == 10: return dt < cutoff   # cutoff.hour is 3-2
    return True



def parse_iso_date_local (datestr, raise_on_error=False):
    """ Parse a ISO 8601 date without a timezone specifier.
    Note: Time zones in ISO 8601 are represented as local time when
    no time zone is given. While it may be safe to assume local time
    when communicating in the same time zone, it is ambiguous when
    used in communicating across different time zones.
    https://en.wikipedia.org/wiki/ISO_8601#Time_zone_designators
    """
    try: return datetime.strptime (datestr, '%Y-%m-%dT%H:%M:%S')
    except ValueError: pass
    try: return datetime.strptime (datestr, '%Y-%m-%dT%H:%M')
    except ValueError: pass
    try: return datetime.strptime (datestr, '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError: pass
    # Note: returns None on error
    #if raise_on_error: raise DateParseError()


def parse_iso_date (datestr):
    """Parse a ISO 8601 combined date and time.
    A Python datetime object is returned, or None on error.
    The returned date is in the local timezone for Norway.
    If date does not contain timezone => assumed to be in local time.
    If date is in zulu => converted to Norwegian local time.
    If date has time zone => no conversion (and assert tz_offset is correct)
    """

    if datestr[-1] == 'Z':
        datestr = datestr[:-1] + '+00:00'

    match = _ISO_DATE_REGEX.match (datestr)
    if not match:
        date = parse_iso_date_local (datestr)
        if date is None: return None
        return date.replace (second=0, microsecond=0) # @todo reuse code bellow
        #return parse_iso_date_local (datestr)  # @todo nuke seconds

    # Regex capture groups
    # \1  g0    datetime-part
    # \2  g1    datetime-part, fraction of seconds (ignored)
    # \3  g2    timezone: + or -
    # \4  g3    timezone: hours
    # \5  g4    timezone: minutes (optional)

    #date = datetime.strptime (match.expand(r'\1'), '%Y-%m-%dT%H:%M:%S') # @todo handle error
    date = parse_iso_date_local (match.expand(r'\1'))
    date = date.replace (second=0, microsecond=0)

    tz_hour = int (match.expand(r'\2\3'))
    tz_min  = int (match.expand(r'\4')) if match.lastindex==4 else 0
    assert tz_hour in (0,1,2)
    assert tz_min == 0

    if tz_hour==0:  # zulu time => convert to local
        date += timedelta (hours = 2 if is_dst(date) else 1)

    return date



# @todo add tests

#from datetime import datetime
#dt = datetime (2015, 10, 25, 01, 59)
#print dt
#print is_dst (dt)
#exit (0)

#print parse_iso_date ('2014-03-07T06:00')
#print parse_iso_date ('2014-03-07T06:00:24')
#print parse_iso_date ('2014-03-07T06:00:24.123')
#
#print parse_iso_date ('2014-03-07T05:00:24Z')       # zulu
#print parse_iso_date ('2014-03-07T05:00:24+00:00')  # zulu
#print parse_iso_date ('2014-03-07T06:00:24+01:00')  # norwegian
#print parse_iso_date ('2014-04-07T04:00:24Z')       # zulu + dst
#
#print parse_iso_date ('2014-03-07T05:00:24.123Z')
#print parse_iso_date ('2014-03-07T05:00:24.123+00:00')
#print parse_iso_date ('2014-03-07T06:00:24.123+01:00')
