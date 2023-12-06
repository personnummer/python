import datetime
import math
import re

string_types = str


class PersonnummerException(Exception):
    pass


class PersonnummerInvalidException(PersonnummerException):
    pass


class PersonnummerParseException(PersonnummerException):
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
        self._parse_parts(ssn)
        self._validate()

    @property
    def parts(self) -> dict:
        return {
            'century': self.century,
            'year': self.year,
            'month': self.month,
            'day': self.day,
            'sep': self.sep,
            'num': self.num,
            'check': self.check,
        }

    def is_coordination_number(self):
        return int(self.day) > 60

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

        return ssn_format.format(
            century=self.century,
            year=self.year,
            month=self.month,
            day=self.day,
            sep=self.sep,
            num=self.num,
            check=self.check,
        )

    def get_date(self):
        """
        Get the underlying date from a social security number

        :rtype: datetime.date
        """
        year = int(self.full_year)
        month = int(self.month)
        day = int(self.day)
        day = day - 60 if self.is_coordination_number() else day
        return datetime.date(year, month, day)

    def get_age(self):
        """
        Get the age of a person from a Swedish personal identity number

        :rtype: int
        :return:
        """
        today = _get_current_date()

        year = int(self.full_year)
        month = int(self.month)
        day = int(self.day)
        day = day - 60 if self.is_coordination_number() else day

        return today.year - year - ((today.month, today.day) < (month, day))

    def is_female(self):
        return not self.is_male()

    def is_male(self):
        gender_digit = int(self.num)

        return gender_digit % 2 != 0

    def _parse_parts(self, ssn):
        """
        Get different parts of a Swedish personal identity number
        :param ssn
        :type ssn str|int
        """
        reg = r"^(\d{2}){0,1}(\d{2})(\d{2})(\d{2})([\-\+]{0,1})?((?!000)\d{3})(\d{0,1})$"
        match = re.match(reg, str(ssn))

        if not match:
            raise PersonnummerParseException(
                'Could not parse "{}" as a valid Swedish SSN.'.format(ssn))

        century = match.group(1)
        year = match.group(2)
        month = match.group(3)
        day = match.group(4)
        sep = match.group(5)
        num = match.group(6)
        check = match.group(7)

        if not century:
            base_year = _get_current_date().year
            if sep == '+':
                base_year -= 100
            else:
                sep = '-'
            full_year = base_year - ((base_year - int(year)) % 100)
            century = str(int(full_year / 100))
        else:
            sep = '-' if _get_current_date().year - int(century + year) < 100 else '+'
        
        self.century = century
        self.full_year = century + year
        self.year = year
        self.month = month
        self.day = day
        self.sep = sep
        self.num = num
        self.check = check

    def _validate(self):
        """
        Validate a Swedish personal identity number
        """
        if len(self.check) == 0:
            raise PersonnummerInvalidException

        is_valid = _luhn(self.year + self.month + self.day + self.num) == int(self.check)
        if not is_valid:
            raise PersonnummerInvalidException

        try:
            self.get_date()
        except ValueError:
            raise PersonnummerInvalidException

    @staticmethod
    def parse(ssn, options=None):
        """
        Returns a new Personnummer object
        :param ssn
        :type ssn str/int
        :param options
        :type options dict
        :rtype: Personnummer
        :return:
        """
        return Personnummer(ssn, options)


def _luhn(data):
    """
    Calculates the Luhn checksum of a string of digits
    :param data
    :type data str
    :rtype: int
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
    :rtype: Personnummer
    :return:
    """
    return Personnummer.parse(ssn, options)


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


def _get_current_date():
    """
    Get current time. The purpose of this function is to be able to mock
    current time during tests

    :return:
    :rtype datetime.datetime:
    """
    return datetime.date.today()
