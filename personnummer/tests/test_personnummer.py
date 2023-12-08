from datetime import date
from unittest import TestCase
from unittest import mock

from personnummer import personnummer
import urllib.request
import json


def get_test_data():
    response = urllib.request.urlopen(
        'https://raw.githubusercontent.com/personnummer/meta/master/testdata/list.json')
    raw = response.read().decode('utf-8')
    return json.loads(raw)


test_data = get_test_data()
availableListFormats = [
    'long_format',
    'short_format',
    'separated_format',
    'separated_long',
]


class TestPersonnummer(TestCase):
    def testPersonnummerList(self):
        for item in test_data:
            for available_format in availableListFormats:
                self.assertEqual(personnummer.valid(
                    item[available_format]), item['valid'])

    def testPersonnummerFormat(self):
        for item in test_data:
            if not item['valid']:
                continue

            expected_long_format = item['long_format']
            expected_separated_format: str = item['separated_format']
            for available_format in availableListFormats:
                if available_format == 'short_format' and '+' in expected_separated_format:
                    # Since the short format is missing the separator,
                    # the library will never use the `+` separator
                    # in the outputted format
                    continue
                self.assertEqual(
                    expected_separated_format,
                    personnummer.parse(item[available_format]).format()
                )
                self.assertEqual(
                    expected_long_format,
                    personnummer.parse(item[available_format]).format(True)
                )

    def testPersonnummerError(self):
        for item in test_data:
            if item['valid']:
                continue

            for available_format in availableListFormats:
                self.assertRaises(
                    personnummer.PersonnummerException,
                    personnummer.parse,
                    item[available_format],
                )

    def testPersonnummerSex(self):
        for item in test_data:
            if not item['valid']:
                continue

            for available_format in availableListFormats:
                self.assertEqual(personnummer.parse(
                    item[available_format]).is_male(), item['isMale'])
                self.assertEqual(personnummer.parse(
                    item[available_format]).is_female(), item['isFemale'])

    def testPersonnummerAge(self):
        for item in test_data:
            if not item['valid']:
                continue

            separated_format = item['separated_format']
            pin = item['separated_long']
            year = int(pin[0:4])
            month = int(pin[4:6])
            day = int(pin[6:8])

            if item['type'] == 'con':
                day -= 60
            if '+' in separated_format:
                # This is needed in order for the age to be the same
                # when testing the 'long_format' and any of the separated_*
                # formats. Otherwise, the long format will have an age of 0
                # and the separated ones will have an age of 100.
                year += 100

            mocked_date = date(year=year, month=month, day=day)
            for available_format in availableListFormats:
                if available_format == 'short_format' and '+' in separated_format:
                    # Since the short format is missing the separator,
                    # the library will never use the `+` separator
                    # in the outputted format
                    continue
                p = personnummer.parse(item[available_format])
                with mock.patch(
                    'personnummer.personnummer._get_current_date',
                    mock.Mock(return_value=mocked_date)
                ):
                    if '+' in separated_format:
                        self.assertEqual(100, p.get_age())
                    else:
                        self.assertEqual(0, p.get_age())
