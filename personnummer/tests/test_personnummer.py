from unittest import TestCase
from personnummer import personnummer


class TestPersonnummer(TestCase):
    def test_with_control_digit(self):
        self.assertTrue(personnummer.valid(6403273813))
        self.assertTrue(personnummer.valid('510818-9167'))
        self.assertTrue(personnummer.valid('851226-2190'))
        self.assertTrue(personnummer.valid('19900101-0017'))
        self.assertTrue(personnummer.valid('19130401+2931'))
        self.assertTrue(personnummer.valid('196408233234'))
        self.assertTrue(personnummer.valid('000101-0107'))
        self.assertTrue(personnummer.valid('0001010107'))
        self.assertTrue(personnummer.valid('200002296127'))
        self.assertTrue(personnummer.valid('200002283422'))

    def test_without_control_digit(self):
        self.assertFalse(personnummer.valid(640327381))
        self.assertFalse(personnummer.valid('510818-916'))
        self.assertFalse(personnummer.valid('19900101-001'))
        self.assertFalse(personnummer.valid('100101+001'))

    def test_wrong_personnummer_or_types(self):
        self.assertFalse(personnummer.valid(None))
        self.assertFalse(personnummer.valid([]))
        self.assertFalse(personnummer.valid({}))
        self.assertFalse(personnummer.valid(False))
        self.assertFalse(personnummer.valid(True))
        self.assertFalse(personnummer.valid(1122334455))
        self.assertFalse(personnummer.valid('112233-4455'))
        self.assertFalse(personnummer.valid('19112233-4455'))
        self.assertFalse(personnummer.valid('9999999999'))
        self.assertFalse(personnummer.valid('199999999999'))
        self.assertFalse(personnummer.valid('9913131315'))
        self.assertFalse(personnummer.valid('9911311232'))
        self.assertFalse(personnummer.valid('9902291237'))
        self.assertFalse(personnummer.valid('19990919_3766'))
        self.assertFalse(personnummer.valid('990919_3766'))
        self.assertFalse(personnummer.valid('199909193776'))
        self.assertFalse(personnummer.valid('Just a string'))
        self.assertFalse(personnummer.valid('990919+3776'))
        self.assertFalse(personnummer.valid('990919-3776'))
        self.assertFalse(personnummer.valid('9909193776'))

    def test_coordination_numbers(self):
        self.assertTrue(personnummer.valid('701063-2391'))
        self.assertTrue(personnummer.valid('640883-3231'))

    def test_exclude_of_coordination_numbers(self):
        self.assertFalse(personnummer.valid('701063-2391', False))
        self.assertFalse(personnummer.valid('640883-3231', False))

    def test_wrong_coordination_numbers(self):
        self.assertFalse(personnummer.valid('900161-0017'))
        self.assertFalse(personnummer.valid('640893-3231'))

    def test_format(self):
        self.assertEqual('640327-3813', personnummer.format(6403273813))
        self.assertEqual('510818-9167', personnummer.format('510818-9167'))
        self.assertEqual('900101-0017', personnummer.format('19900101-0017'))
        self.assertEqual('130401+2931', personnummer.format('19130401+2931'))
        self.assertEqual('640823-3234', personnummer.format('196408233234'))
        self.assertEqual('000101-0107', personnummer.format('0001010107'))
        self.assertEqual('000101-0107', personnummer.format('000101-0107'))
        self.assertEqual('130401+2931', personnummer.format('191304012931'))
        self.assertEqual('196403273813', personnummer.format(6403273813, True))
        self.assertEqual('195108189167', personnummer.format('510818-9167', True))
        self.assertEqual('199001010017', personnummer.format('19900101-0017', True))
        self.assertEqual('191304012931', personnummer.format('19130401+2931', True))
        self.assertEqual('196408233234', personnummer.format('196408233234', True))
        self.assertEqual('200001010107', personnummer.format('0001010107', True))
        self.assertEqual('200001010107', personnummer.format('000101-0107', True))
        self.assertEqual('190001010107', personnummer.format('000101+0107', True))
        self.assertRaises(ValueError, personnummer.format, "19990919_3766")

    def test_format_right_separator(self):
        self.assertEqual('130401+2931', personnummer.format('19130401-2931'))
        self.assertEqual('900101-0017', personnummer.format('19900101+0017'))
        self.assertEqual('121212+1212', personnummer.format('19121212-1212'))
        self.assertEqual('121212-1212', personnummer.format('20121212+1212'))
