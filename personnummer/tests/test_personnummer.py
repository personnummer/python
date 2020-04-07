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


