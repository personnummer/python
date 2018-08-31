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

# luhn will test if the given string is a valid luhn string.
def luhn(s):
    v = 0
    sum = 0

    for i in range(0, len(s)):
        v = int(s[i])
        v *= 2 - (i % 2)
        if v > 9:
            v -= 9
        sum += v
    
    return int(math.ceil(float(sum)/10) * 10 - float(sum))

# testDate will test if date is valid or not.
def testDate(year, month, day):
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

# valid will validate Swedish social security numbers.
def valid(s):
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
        year = year[2:]

    valid = luhn(year + month + day + num) == int(check)

    if valid and testDate(year, int(month), int(day)):
        return True

    return valid and testDate(year, int(month), int(day) - 60)