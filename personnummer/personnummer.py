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

def luhn(s):
    """
    Test if the input string is a valid Luhn string.
    :param s:
    :return:
    """
    v = 0
    sum = 0

    for i in range(0, len(s)):
        v = int(s[i])
        v *= 2 - (i % 2)
        if v > 9:
            v -= 9
        sum += v

    return int(math.ceil(float(sum)/10) * 10 - float(sum))

def _test_date(year, month, day):
    """
    Test if the input parameters are a valid date or not
    """
    for x in ['19', '20']:
        newy = x.__str__() + year.__str__()
        newy = int(newy)
        try:
            date = datetime.date(newy, month, day)
            if (date.year != newy or date.month != month or date.day != day) == False:
                return True
        except ValueError:
            continue

    return False

def valid(s, include_coordination_number=True):
    """
    Validate Swedish social security numbers

    :param s: A Swedish social security number to validate
    :param include_coordination_number: Set to False in order to exclude
        coordination number (Samordningsnummer) from validation
    :type s: str|int
    :type include_coordination_number: bool
    :rtype: bool
    :return:
    """
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

    valid = luhn(year + month + day + num) == int(check)

    if valid and _test_date(year, int(month), int(day)):
        return True

    if not include_coordination_number:
        return False

    return valid and _test_date(year, int(month), int(day) - 60)
