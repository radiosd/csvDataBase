
"""
    Using unittest to validate code for CsvItem class    
                                                         rgr04jun18
    look for #!# lines where corrections are pending
"""
from __future__ import print_function

import unittest
from rgrCsvData.csvDataBase import CsvItem

TEST_KEYS = ('key1', 'key2', 'keys')
TEST_VALUES2 = ['11', '2', '3', '4']
TEST_OUTPUT1 = 'key1: 11'
TEST_OUTPUT2 = ['2', '11']                  # pick test
TEST_OUTPUT3 = {'key2': '2', 'key1': '11'}  # extract test

class TestCsvItem(unittest.TestCase):

    def setUp(self):
        self.longMessage = True  # enables "test != result" in error message

    def createInst(self):
        inst = CsvItem(TEST_KEYS)
        inst.read(TEST_VALUES2)
        return inst
    
    # everything starting test is run, but in no guaranteed order
    #!# There is no doc string for the Class definition
    def testCreateInstance(self):
        """check creation of an ordered dict with TEST_KEYS"""
        # also checks the read() and isList() functions
        inst = CsvItem(TEST_KEYS)
        self.assertEqual(inst['key1'], '', 'initial values are blank')
        self.assertTrue(inst.isList('keys'), 'last key is a list')
        # populate the dict with values
        inst.read(['1'])
        self.assertEqual(inst['key1'], '1', 'given values set by read')
        self.assertEqual(inst['key2'], '', 'missing values not set by read')
        self.assertListEqual(inst['keys'], [], 'last key is an empty list')
        inst.read(TEST_VALUES2)
        self.assertEqual(inst['key1'], '11', 'read over writes earlier values')
        self.assertEqual(inst['key2'], '2', 'read over writes earlier values')
        self.assertListEqual(inst['keys'], ['3','4'],
                             'list value takes all exta items in read')
        # re-reading things stay the same (list is not addede to)
        inst.read(TEST_VALUES2)
        self.assertListEqual(inst['keys'], ['3','4'],
                             'list value takes all exta items in read')

    def testOutputFunctions(self):
        """check the output functions and formatting"""
        inst = self.createInst()
        # also check findKey() function
        # valueStr() function
        width = 4
        ans = inst['key1']
        ans = ans + (width - len(ans))*' '
        self.assertEqual(inst.valueStrf('key1', width), ans,
                         'width format is left justified')
        #!# no test for a value > format width
        self.assertListEqual(inst.pick('key2', 'key1'), TEST_OUTPUT2,
                             'pick values by key field name')
        self.assertDictEqual(inst.extract('key2', 'key1'), TEST_OUTPUT3,
                             'extract values by key field name')

    def testCsvInterface(self):
        """check read and write from a csv file"""
        inst = self.createInst()
        self.assertListEqual(inst.write(), TEST_VALUES2,
                             'return heading for csv file format')
        #!# output function should use findKey()
        #!# output function has no doc string
        self.assertEqual(inst.output('key1'), TEST_OUTPUT1,
                         'output() returns key: value format')
from os import path
print('\nTesting class CsvItem in module:\n',path.abspath(CsvItem.__module__))

if __name__=='__main__':
    unittest.main()
    
