from datetime import datetime
from unittest import TestCase
from personnummer import personnummer
import urllib.request
import json

def get_test_data():
    response = urllib.request.urlopen('https://raw.githubusercontent.com/personnummer/meta/master/testdata/list.json')
    raw = response.read().decode('utf-8')
    return json.loads(raw)

test_data = get_test_data()
availableListFormats = [
  "long_format",
  "short_format",
  "separated_format",
  "separated_long",
]

class TestPersonnummer(TestCase):
    def testPersonnummerList(self):
        for item in test_data:
            for format in availableListFormats:
                self.assertEqual(personnummer.valid(item[format]), item['valid'])

    def testPersonnummerFormat(self):
        for item in test_data:
            for format in availableListFormats:
                if format != "short_format" and item['separated_format'].find('+') != -1:
                    self.assertEqual(personnummer.parse(item[format]).format(), item['separated_format'])
                    self.assertEqual(personnummer.parse(item[format]).format(True), item['long_format'])

    def testPersonnummerError(self):
        for item in test_data:
            for format in availableListFormats:
                if item['valid']:
                    return

                try:
                    personnummer.parse(item[format])
                    self.assertTrue(False)
                except:
                    self.assertTrue(True)

    def testPersonnummerSex(self):
        for item in test_data:
            for format in availableListFormats:
                if not item['valid']:
                    return

                self.assertEqual(personnummer.parse(item[format]).isMale(), item['isMale'])
                self.assertEqual(personnummer.parse(item[format]).isFemale(), item['isFemale'])

#    def test_get_age(self):
#        self.assertEqual(34, personnummer.parse('198507099805').get_age())
#        self.assertEqual(34, personnummer.parse('198507099813').get_age())
#        self.assertEqual(54, personnummer.parse('196411139808').get_age())
#        self.assertEqual(106, personnummer.parse('19121212+1212').get_age())
