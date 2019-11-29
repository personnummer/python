from datetime import datetime
from unittest import TestCase

import mock

from personnummer import personnummer


@mock.patch(
    'personnummer.personnummer._get_current_datetime',
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

    def test_exclude_of_coordination_numbers(self):
        self.assertFalse(personnummer.valid('198507699802', False))
        self.assertFalse(personnummer.valid('198507699810', False))

    def test_wrong_coordination_numbers(self):
        self.assertFalse(personnummer.valid('198567099805'))

    def test_format(self):
        self.assertEqual('850709-9805', personnummer.format('19850709-9805'))
        self.assertEqual('850709-9813', personnummer.format('198507099813'))
        self.assertEqual('198507099805', personnummer.format('19850709-9805', True))
        self.assertEqual('198507099813', personnummer.format('198507099813', True))

    def test_format_right_separator(self):
        self.assertEqual('850709-9805', personnummer.format('19850709+9805'))
        self.assertEqual('121212+1212', personnummer.format('19121212-1212'))

    def test_format_with_invalid_numbers(self):
        self.assertRaises(ValueError, personnummer.format, None)
        self.assertRaises(ValueError, personnummer.format, [])
        self.assertRaises(ValueError, personnummer.format, {})
        self.assertRaises(ValueError, personnummer.format, False)
        self.assertRaises(ValueError, personnummer.format, True)
        self.assertRaises(ValueError, personnummer.format, 0)
        self.assertRaises(ValueError, personnummer.format, '19112233-4455')
        self.assertRaises(ValueError, personnummer.format, '20112233-4455')
        self.assertRaises(ValueError, personnummer.format, '9999999999')
        self.assertRaises(ValueError, personnummer.format, '199999999999')
        self.assertRaises(ValueError, personnummer.format, '199909193776')
        self.assertRaises(ValueError, personnummer.format, 'Just a string')
