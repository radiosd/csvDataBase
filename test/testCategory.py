
"""
    Using unittest to validate code for Category class in findAdex.  
                                                         rgr05jun18
    look for #!# lines where corrections are pending
"""
from __future__ import print_function

import unittest
from rgrCsvData.findAdex import Category, ALL_FIELDS

class TestCategory(unittest.TestCase):

    def setUp(self):
        self.longMessage = True  # enables "test != result" in error message

    def tearDown(self):
        pass

    def createInstance(self):
        return Category(ALL_FIELDS)

    # everything starting test is run, but in no guaranteed order    
    def testModifyFields(self):
        """check ability to have required and optional fields"""
        inst = self.createInstance()

##    def testAnother(self):
##        pass

from os import path
print('\nTesting class Category in module:\n',path.abspath(Category.__module__))

if __name__=='__main__':
    unittest.main()
    
