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

    def test_wrong_coordination_numbers(self):
        self.assertFalse(personnummer.valid('900161-0017'))
        self.assertFalse(personnummer.valid('640893-3231'))

    def test_format_short_with_control_digit(self):
        self.assertEqual('640327-3813', personnummer.format_short(6403273813))
        self.assertEqual('510818-9167', personnummer.format_short('510818-9167'))
        self.assertEqual('851226-2190', personnummer.format_short('851226-2190'))
        self.assertEqual('900101-0017', personnummer.format_short('19900101-0017'))
        self.assertEqual('130401+2931', personnummer.format_short('19130401+2931'))
        self.assertEqual('640823-3234', personnummer.format_short('196408233234'))
        self.assertEqual('000101-0107', personnummer.format_short('000101-0107'))
        self.assertEqual('000101-0107', personnummer.format_short('0001010107'))
        self.assertEqual('000229-6127', personnummer.format_short('200002296127'))
        self.assertEqual('000228-3422', personnummer.format_short('200002283422'))
        self.assertEqual('701063-2391', personnummer.format_short('701063-2391'))
        self.assertEqual('640883-3231', personnummer.format_short('640883-3231'))
    def test_format_long_with_control_digit(self):
        self.assertEqual('196403273813', personnummer.format_long(6403273813))
        self.assertEqual('195108189167', personnummer.format_long('510818-9167'))
        self.assertEqual('198512262190', personnummer.format_long('851226-2190'))
        self.assertEqual('199001010017', personnummer.format_long('19900101-0017'))
        self.assertEqual('191304012931', personnummer.format_long('19130401+2931'))
        self.assertEqual('191304012931', personnummer.format_long('130401+2931'))
        self.assertEqual('201304012931', personnummer.format_long('1304012931'))
        self.assertEqual('196408233234', personnummer.format_long('196408233234'))
        self.assertEqual('200001010107', personnummer.format_long('000101-0107'))
        self.assertEqual('200001010107', personnummer.format_long('0001010107'))
        self.assertEqual('200002296127', personnummer.format_long('200002296127'))
        self.assertEqual('200002283422', personnummer.format_long('200002283422'))
        self.assertEqual('197010632391', personnummer.format_long('701063-2391'))
        self.assertEqual('196408833231', personnummer.format_long('640883-3231'))

