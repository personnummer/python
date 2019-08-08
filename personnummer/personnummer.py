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
    Calculates the Luhn checksum of a string of digits
    :param s:
    :type s: str
    :return:
    """
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
            if not (date.year != newy or date.month != month or date.day != day):
                return True
        except ValueError:
            continue

    return False


def _get_parts(ssn):
    """
    Get different parts of a Swedish social security number
    :param ssn: A Swedish social security number to format
    :type ssn: str|int
    :rtype: dict
    :return: Returns a dictionary of the different parts of a Swedish SSN.
        The dict keys are:
        'century', 'year', 'month', 'day', 'sep', 'num', 'check'
    """
    reg = r"^(\d{2}){0,1}(\d{2})(\d{2})(\d{2})([\-|\+]{0,1})?(\d{3})(\d{0,1})$"
    match = re.match(reg, str(ssn))

    if not match:
        raise ValueError(
            'Could not parse "{}" as a valid Swedish SSN.'.format(ssn))

    century = match.group(1)
    year = match.group(2)
    month = match.group(3)
    day = match.group(4)
    sep = match.group(5)
    num = match.group(6)
    check = match.group(7)

    if sep == '':
        if not century:
            sep = '-'
        elif datetime.datetime.now().year - int(century + year) < 100:
            sep = '-'
        else:
            sep = '+'

    if not century:
        base_year = datetime.datetime.now().year
        if sep == '+':
            base_year = base_year - 100
        full_year = base_year - ((base_year - int(year)) % 100)
        century = str(int(full_year / 100))

    return {
        'century': century,
        'year': year,
        'month': month,
        'day': day,
        'sep': sep,
        'num': num,
        'check': check
    }


def valid(s, include_coordination_number=True):
    """
    Validate a Swedish social security number

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

    try:
        parts = _get_parts(s)
    except ValueError:
        return False

    year = parts['year']
    month = parts['month']
    day = parts['day']
    num = parts['num']
    check = parts['check']

    if len(check) == 0:
        return False

    is_valid = luhn(year + month + day + num) == int(check)

    if is_valid and _test_date(year, int(month), int(day)):
        return True

    if not include_coordination_number:
        return False

    return is_valid and _test_date(year, int(month), int(day) - 60)


def format(ssn, long_format=False):
    """
    Format a Swedish social security number as one of the official formats,
    A long format or a short format.

    This function raises a ValueError if the input number could not be parsed
    as a valid Swedish social security number

    :param ssn: A Swedish social security number to format
    :param long_format: Defaults to False and formats a social security number
        as YYMMDD-XXXX. If set to True the format will be YYYYMMDDXXXX.
    :type ssn: str|int
    :type long_format: bool
    :rtype: str
    :return:
    """

    if not valid(ssn):
        raise ValueError(
            'The social security number "{}" is not valid '
            'and cannot be formatted.'.format(ssn)
        )

    if long_format:
        ssn_format = '{century}{year}{month}{day}{num}{check}'
    else:
        ssn_format = '{year}{month}{day}{sep}{num}{check}'

    parts = _get_parts(ssn)
    return ssn_format.format(**parts)
