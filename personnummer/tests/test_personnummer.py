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
