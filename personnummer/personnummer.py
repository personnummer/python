import datetime
import math
import numbers
import re
import sys

PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str
else:
    string_types = basestring


class Personnummer:
    def __init__(self, century, year, month, day, sep, num, check):
        self.century = century
        self.year = year
        self.month = month
        self.day = day
        self.sep = sep
        self.num = num
        self.check = check


# luhn will test if the given string is a valid luhn string.
def luhn(s):
    control_sum = 0

    for i in range(0, len(s)):
        v = int(s[i])
        v *= 2 - (i % 2)
        if v > 9:
            v -= 9
        control_sum += v

    return int(math.ceil(float(control_sum) / 10) * 10 - float(control_sum))


# test_date will test if date is valid or not.
def test_date(year, month, day):
    for x in ['19', '20']:
        newy = x.__str__() + year.__str__()
        newy = int(newy)
        try:
            date = datetime.date(newy, month, day)
            if not (date.year != newy or date.month != month or date.day != day):
                return True
        except ValueError:
            continue

    return False


def test_in_future(century, year, month, day):
    try:
        date = datetime.datetime(int(century.__str__() + year.__str__()), int(month), int(day))
    except ValueError:
        date = datetime.datetime(int(century.__str__() + year.__str__()), int(month), int(day) - 60)
    if date > datetime.datetime.now():
        return True
    else:
        return False


def test_100_years_ago(century, year, month, day):
    try:
        date = datetime.datetime(int(century.__str__() + year.__str__()), int(month), int(day))
    except ValueError:
        date = datetime.datetime(int(century.__str__() + year.__str__()), int(month), int(day) - 60)
    difference = datetime.datetime.now() - date
    difference_in_years = (difference.days + difference.seconds / 86400) / 365.2425
    if difference_in_years > 100:
        return True
    else:
        return False


# valid will validate Swedish social security numbers.
def valid(s):
    p = parse(s)
    if not p:
        return False
    return validate(p)


def validate(p):
    is_valid = luhn(p.year + p.month + p.day + p.num) == int(p.check)

    if is_valid and test_date(p.year, int(p.month), int(p.day)):
        return True

    return is_valid and test_date(p.year, int(p.month), int(p.day) - 60)


def parse(s):
    if isinstance(s, string_types) is False and isinstance(s, numbers.Integral) is False:
        return False

    reg = "^(\d{2}){0,1}(\d{2})(\d{2})(\d{2})([\-|\+]{0,1})?(\d{3})(\d{0,1})$"
    match = re.match(reg, s.__str__())

    if not match:
        return False

    century = match.group(1)
    year    = match.group(2)
    month   = match.group(3)
    day     = match.group(4)
    sep     = match.group(5)
    num     = match.group(6)
    check   = match.group(7)

    if len(check) == 0:
        return False

    if len(year) == 4:
        century = year[0:1]
        year = year[2:]

    try:
        if not sep:
            if not century:
                if test_in_future('20', year, month, day):
                    century = '19'
                    if test_100_years_ago('19', year, month, day):
                        sep = '+'
                    else:
                        sep = '-'
                else:
                    century = '20'
                    sep = '-'
            else:
                if test_100_years_ago(century, year, month, day):
                    sep = '+'
                else:
                    sep = '-'
        if not century:
            if test_in_future('20', year, month, day):
                century = '19'
            else:
                if sep == '+':
                    century = '19'
                else:
                    century = '20'
        return Personnummer(century, year, month, day, sep, num, check)
    except ValueError:
        return False


def format_short(s):
    p = parse(s)
    if not validate(p):
        return False
    return "%s%s%s%s%s%s" % (p.year, p.month, p.day, p.sep, p.num, p.check)


def format_long(s):
    p = parse(s)
    if not validate(p):
        return False

    return "%s%s%s%s%s%s" % (p.century, p.year, p.month, p.day, p.num, p.check)

