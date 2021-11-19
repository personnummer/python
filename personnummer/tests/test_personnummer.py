from datetime import datetime
from unittest import TestCase
from personnummer import personnummer
import urllib.request
import json
import mock


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
            for format in availableListFormats:
                self.assertEqual(personnummer.valid(
                    item[format]), item['valid'])

    def testPersonnummerFormat(self):
        for item in test_data:
            if not item['valid']:
                return

            for format in availableListFormats:
                if format != 'short_format':
                    self.assertEqual(personnummer.parse(
                        item[format]).format(), item['separated_format'])
                    self.assertEqual(personnummer.parse(
                        item[format]).format(True), item['long_format'])

    def testPersonnummerError(self):
        for item in test_data:
            if item['valid']:
                return

            for format in availableListFormats:
                try:
                    personnummer.parse(item[format])
                    self.assertTrue(False)
                except:
                    self.assertTrue(True)

    def testPersonnummerSex(self):
        for item in test_data:
            if not item['valid']:
                return

            for format in availableListFormats:
                self.assertEqual(personnummer.parse(
                    item[format]).isMale(), item['isMale'])
                self.assertEqual(personnummer.parse(
                    item[format]).isFemale(), item['isFemale'])

    def testPersonnummerAge(self):
        for item in test_data:
            if not item['valid']:
                return

            for format in availableListFormats:
                if format != 'short_format':
                    pin = item['separated_long']
                    year = int(pin[0:4])
                    month = int(pin[4:6])
                    day = int(pin[6:8])

                    if item['type'] == 'con':
                        day -= 60

                    date = datetime(year=year, month=month, day=day)
                    p = personnummer.parse(item[format])

                    with mock.patch('personnummer.personnummer.get_current_datetime', mock.Mock(return_value=date)):
                        self.assertEqual(0, p.get_age())
