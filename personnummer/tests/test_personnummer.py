from datetime import datetime
from unittest import TestCase

import mock

import urllib.request
import json

from personnummer import personnummer


def get_test_data():
    response = urllib.request.urlopen('https://raw.githubusercontent.com/personnummer/meta/master/testdata/list.json')
    raw = response.read().decode('utf-8')

    list_dict = json.loads(raw)

    return list_dict


test_data = get_test_data()


@mock.patch(
    'personnummer.personnummer.get_current_datetime',
    mock.Mock(return_value=datetime.fromtimestamp(1565704890)))
class TestPersonnummer(TestCase):
    def valid_(self, format_type):
        for datum in test_data:
            self.assertEqual(personnummer.valid(datum[format_type]), datum['valid'])

    def test_integer(self):
        self.valid_('integer')

    def test_long_format(self):
        self.valid_('long_format')

    def test_short_format(self):
        self.valid_('short_format')

    def test_separated_format(self):
        self.valid_('separated_format')

    def test_separated_long(self):
        self.valid_('separated_long')

    def test_is_male(self):
        for datum in test_data:
            if datum['valid']:
                tmp = personnummer.parse(datum['long_format'])
                self.assertEqual(tmp.is_male(), datum['isMale'])

    def test_is_female(self):
        for datum in test_data:
            if datum['valid']:
                tmp = personnummer.parse(datum['long_format'])
                self.assertEqual(tmp.is_female(), datum['isFemale'])

    def test_get_age(self):
        self.assertEqual(34, personnummer.parse('198507099805').get_age())
        self.assertEqual(34, personnummer.parse('198507099813').get_age())
        self.assertEqual(54, personnummer.parse('196411139808').get_age())
        self.assertEqual(106, personnummer.parse('19121212+1212').get_age())

    def test_coordination_numbers(self):
        p1 = personnummer.parse('198507699810')
        self.assertEqual(34, p1.get_age())
        self.assertEqual(True, p1.is_coordination_number())

        p2 = personnummer.parse('198507699802')
        self.assertEqual(34, p2.get_age())
        self.assertEqual(True, p2.is_coordination_number())

        p3 = personnummer.parse('198507099805')
        self.assertEqual(34, p3.get_age())
        self.assertEqual(False, p3.is_coordination_number())

