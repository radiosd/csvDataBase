
"""
    Using unittest to validate code for Catalogue class 
                                                         rgr06jun18
    look for #!# lines where corrections are pending
"""
from __future__ import print_function

import unittest
from rgrCsvData.catalogue import Catalogue, Reference

TEST_DB_FILE = 'test/PapersDB'
TEST_DB_COUNT = 9

class TestCatalogue(unittest.TestCase):

    def setUp(self):
        self.longMessage = True  # enables "test != result" in error message

    def tearDown(self):
        pass

    def createInstance(self):
        return Catalogue(TEST_DB_FILE)

    # everything starting test is run, but in no guaranteed order    
    def testCreateInstance(self):
        """check creation of DB instance"""
        inst = self.createInstance()
        self.assertEqual(len(inst), TEST_DB_COUNT,
                         'confirm the DB is loaded')
        self.assertIs(inst.data.itemClass, Reference,
                         'correct set up of DB type')
        item = inst.data[0]
        self.assertEqual(item.__class__.__name__, 'Reference',
                         'correct instance sub-class type')
        #!# The archive field should be boolean, but ends up as a string

    def testAnother(self):
        pass

from os import path
print('\nTesting Catalogue class in module:\n',
      path.abspath(Catalogue.__module__))

if __name__=='__main__':
    unittest.main()
    
