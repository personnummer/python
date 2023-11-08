import datetime
import math
import re

string_types = str


class PersonnummerException(Exception):
    pass


class Personnummer:
    def __init__(self, ssn, options=None):
        """
        Initializes the Object and checks if the given Swedish personal identity number is valid.
        :param ssn
        :type ssn str
        :param options
        :type options dict
        """

        if options is None:
            options = {}

        self.options = options
        self._ssn = ssn
        self.parts = self.get_parts(ssn)

        if self.valid() is False:
            raise PersonnummerException(
                str(ssn) + ' Not a valid Swedish personal identity number!')

    def format(self, long_format=False):
        """
        Format a Swedish personal identity number as one of the official formats,
        A long format or a short format.

        This function raises a ValueError if the input number could not be parsed
        as a valid Swedish personal identity number

        :param long_format: Defaults to False and formats a personal identity number
            as YYMMDD-XXXX. If set to True the format will be YYYYMMDDXXXX.
        :type long_format: bool
        :rtype: str
        :return:
        """

        if long_format:
            ssn_format = '{century}{year}{month}{day}{num}{check}'
        else:
            ssn_format = '{year}{month}{day}{sep}{num}{check}'

        return ssn_format.format(**self.parts)

    def get_age(self):
        """
        Get the age of a person from a Swedish personal identity number

        :rtype: int
        :return:
        """
        today = get_current_datetime()

        year = int('{century}{year}'.format(
            century=self.parts['century'],
            year=self.parts['year'])
        )
        month = int(self.parts['month'])
        day = int(self.parts['day'])
        if self.is_coordination_number():
            day -= 60

        return today.year - year - ((today.month, today.day) < (month, day))

    def is_female(self):
        return not self.is_male()

    def is_male(self):
        gender_digit = self.parts['num']

        return int(gender_digit) % 2 != 0

    def is_coordination_number(self):
        return test_date(
            int(self.parts['century'] + self.parts['year']),
            int(self.parts['month']),
            int(self.parts['day']) - 60,
        )

    @staticmethod
    def get_parts(ssn):
        """
        Get different parts of a Swedish personal identity number
        :rtype: dict
        :return: Returns a dictionary of the different parts of a Swedish SSN.
            The dict keys are:
            'century', 'year', 'month', 'day', 'sep', 'num', 'check'
        """
        reg = r"^(\d{2}){0,1}(\d{2})(\d{2})(\d{2})([\-\+]{0,1})?((?!000)\d{3})(\d{0,1})$"
        match = re.match(reg, str(ssn))

        if not match:
            raise PersonnummerException(
                'Could not parse "{}" as a valid Swedish SSN.'.format(ssn))

        century = match.group(1)
        year = match.group(2)
        month = match.group(3)
        day = match.group(4)
        sep = match.group(5)
        num = match.group(6)
        check = match.group(7)

        if not century:
            base_year = get_current_datetime().year
            if sep == '+':
                base_year -= 100
            else:
                sep = '-'
            full_year = base_year - ((base_year - int(year)) % 100)
            century = str(int(full_year / 100))
        else:
            sep = '-' if get_current_datetime().year - int(century + year) < 100 else '+'
        return {
            'century': century,
            'year': year,
            'month': month,
            'day': day,
            'sep': sep,
            'num': num,
            'check': check
        }

    def valid(self):
        """
        Validate a Swedish personal identity number
        :rtype: bool
        :return:
        """

        century = self.parts['century']
        year = self.parts['year']
        month = self.parts['month']
        day = self.parts['day']
        num = self.parts['num']
        check = self.parts['check']

        if len(check) == 0:
            return False

        is_valid = luhn(year + month + day + num) == int(check)

        if is_valid and test_date(int(century + year), int(month), int(day)):
            return True

        return is_valid and test_date(int(century + year), int(month), int(day) - 60)


def luhn(data):
    """
    Calculates the Luhn checksum of a string of digits
    :return:
    """
    calculation = 0

    for i in range(len(data)):
        v = int(data[i])
        v *= 2 - (i % 2)
        if v > 9:
            v -= 9
        calculation += v

    return int(math.ceil(float(calculation) / 10) * 10 - float(calculation))


def parse(ssn, options=None):
    """
    Returns a new Personnummer object
    :param ssn
    :type ssn str/int
    :param options
    :type options dict
    :rtype: object
    :return: Personnummer object
    """
    if options is None:
        options = {}
    return Personnummer(ssn, options)


def valid(ssn):
    """
    Checks if a ssn is a valid Swedish personal identity number
    :param ssn A Swedish personal identity number
    :type ssn str/int
    """
    try:
        parse(ssn)
        return True
    except PersonnummerException:
        return False


def get_current_datetime():
    """
    Get current time. The purpose of this function is to be able to mock
    current time during tests

    :return:
    :rtype datetime.datetime:
    """
    return datetime.datetime.now()


def test_date(year, month, day):
    """
    Test if the input parameters are a valid date or not
    """
    try:
        date = datetime.date(year, month, day)
        return date.year == year and date.month == month and date.day == day
    except ValueError:
        return False
