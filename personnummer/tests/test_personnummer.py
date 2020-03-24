from datetime import datetime
from unittest import TestCase

import mock

from personnummer import personnummer


@mock.patch(
    'personnummer.personnummer.get_current_datetime',
    mock.Mock(return_value=datetime.fromtimestamp(1565704890)))
class TestPersonnummer(TestCase):

    def test_with_control_digit(self):
        self.assertTrue(personnummer.valid(8507099805))
        self.assertTrue(personnummer.valid('198507099805'))
        self.assertTrue(personnummer.valid('198507099813'))
        self.assertTrue(personnummer.valid('850709-9813'))
        self.assertTrue(personnummer.valid('196411139808'))

    def test_without_control_digit(self):
        self.assertFalse(personnummer.valid('19850709980'))
        self.assertFalse(personnummer.valid('19850709981'))
        self.assertFalse(personnummer.valid('19641113980'))

    def test_wrong_personnummer_or_types(self):
        self.assertFalse(personnummer.valid(None))
        self.assertFalse(personnummer.valid([]))
        self.assertFalse(personnummer.valid({}))
        self.assertFalse(personnummer.valid(False))
        self.assertFalse(personnummer.valid(True))
        self.assertFalse(personnummer.valid(0))
        self.assertFalse(personnummer.valid('19112233-4455'))
        self.assertFalse(personnummer.valid('20112233-4455'))
        self.assertFalse(personnummer.valid('9999999999'))
        self.assertFalse(personnummer.valid('199999999999'))
        self.assertFalse(personnummer.valid('199909193776'))
        self.assertFalse(personnummer.valid('Just a string'))

    def test_coordination_numbers(self):
        self.assertTrue(personnummer.valid('198507699802'))
        self.assertTrue(personnummer.valid('850769-9802'))
        self.assertTrue(personnummer.valid('198507699810'))
        self.assertTrue(personnummer.valid('850769-9810'))

    def test_wrong_coordination_numbers(self):
        self.assertFalse(personnummer.valid('198567099805'))

    def test_format(self):
        data = {
            '850709-9805': '19850709-9805',
            '850709-9813': '198507099813',
        }

        data_long = {
            '198507099805': '19850709-9805',
            '198507099813': '198507099813',
        }

        for ssn in data.keys():
            tmp = personnummer.parse(data[ssn])
            self.assertEqual(ssn, tmp.format())

        for ssn in data_long.keys():
            tmp = personnummer.parse(data_long[ssn])
            self.assertEqual(ssn, tmp.format(True))

    def test_format_right_separator(self):
        data = {
            '850709-9805': '19850709+9805',
            '121212+1212': '19121212-1212',
        }

        for ssn in data.keys():
            tmp = personnummer.parse(data[ssn])
            self.assertEqual(ssn, tmp.format())

    def test_get_age(self):
        data = {
            55: 6403273813,
            67: '510818-9167',
            29: '19900101-0017',
            106: '19130401+2931',
        }

        for age in data.keys():
            tmp = personnummer.parse(data[age])
            self.assertEqual(age, tmp.get_age())

    def test_is_male(self):
        data = {
            196608119894: True,
            '7704089981': False,
        }

        for ssn in data.keys():
            tmp = personnummer.parse(ssn)
            self.assertEqual(data[ssn], tmp.is_male())

    def test_is_female(self):
        data = {
            196608119894: False,
            '7704089981': True,
        }

        for ssn in data.keys():
            tmp = personnummer.parse(ssn)
            self.assertEqual(data[ssn], tmp.is_female())
