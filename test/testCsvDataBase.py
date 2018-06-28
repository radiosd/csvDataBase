
"""
    Using unittest to validate code for .....  
                                                         rgr....18
    look for #!# lines where corrections are pending
"""
from __future__ import print_function

import unittest
from rgrCsvData.csvDataBase import CsvItem, CsvDataBase

DATA_FILE = 'test/BasicDB'
RECORD_COUNT = 4
RECORD_NAMES = ['key1', 'key2', 'keys']

class TestCsvDataBaseClass(unittest.TestCase):

    def setUp(self):
        self.longMessage = True  # enables "test != result" in error message

    def createInstance(self, data_file=DATA_FILE):
        # also checks operation of load()
        return CsvDataBase(data_file)

    def tearDown(self):
        pass

    # everything starting test is run, but in no guaranteed order    
    def testInstanceCreation(self):
        """confirm creation of the simple test db"""
        inst = self.createInstance()
        self.assertEqual(len(inst), RECORD_COUNT,
                         'created correct number of records')
        self.assertIsInstance(inst[0], CsvItem,
                         'db instance is indexable')
        self.assertListEqual(inst.field_names, RECORD_NAMES,
                          'correct filed names')
        # some of these may seem trivial
        self.assertNotEqual(inst.time_stamp, 0, 'time_stamp set')
        #self.assertIsNone(inst.indexed, 'db has no index yet')

    def testFindKeyFunction(self):
        """confirm findKey function operation"""
        inst = self.createInstance()
        self.assertRaises(KeyError, inst.findKey, 'Ky',
                             'throw exception for invalid keys')
        self.assertEqual(inst.findKey('Ke'), 'key1',
                         'find first match regardless of case')
        self.assertListEqual(inst.findKey('Ke', first=False),
                             ['key1', 'key2', 'keys'],
                             'or multiple matches regardless of case')
        self.assertEqual(inst.findKey('Ke'), 'key1',
                         'find first match regardless of case')
        
    def testSeachFunction(self):
        """confirm search function operation"""
        inst = self.createInstance()
        ans = inst.search('key2', 'two')
        self.assertEqual(len(ans), 3, 'this finds only none blankc items')
        ans = inst.search('key2', 'twob')
        self.assertEqual(len(ans), 1, 'insensitive to case finds one entry')
        ans = inst.search('key2', 'twob', False)
        self.assertEqual(len(ans), 0, 'sensitive to case finds no entry')
        
from os import path
print('\nTesting class CsvDataBase in module:\n',path.abspath(CsvDataBase.__module__))

if __name__=='__main__':
    unittest.main()
    print('Tests to be added:')
    print('    db save function')
    print('    db output functions, where interface is yet to be decided')
