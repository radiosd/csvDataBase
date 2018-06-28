
"""
    Using unittest to validate code for FindAdex class  
                                                         rgr05jun18
    look for #!# lines where corrections are pending
"""
from __future__ import print_function

import unittest
from rgrCsvData.findAdex import FindAdex, Category

TEST_DB_FILE = 'test/CategoriesDB'
TEST_DB_COUNT = 32

class TestFindAdex(unittest.TestCase):

    def setUp(self):
        self.longMessage = True  # enables "test != result" in error message

    def tearDown(self):
        pass

    def createInstance(self):
        return FindAdex(TEST_DB_FILE)

    # everything starting test is run, but in no guaranteed order    
    def testCreateInstance(self):
        """create an instance using the test DB"""
        inst = self.createInstance()
        self.assertEqual(len(inst.data), TEST_DB_COUNT,
                           'confirm the DB is loaded')
        self.assertIs(inst.itemClass, Category, 'correct set up of DB type')
        self.assertIsInstance(inst.data[0], Category, 'correct set up of DB type')
        self.assertEqual(inst.data[0]['Category'], '_100',
                         'check first entry is correct')
        

    def testQueryContent(self):
        """check methods to access and verify DB content"""
        inst = self.createInstance()
        self.assertTrue(inst.hasCategory('b301'),
                        'finds category regarless of case')
        self.assertEqual(inst.nextCategory('b3xx'), 'B302',
                         'correct next category available')
        ans = inst.listCategories('_')
        self.assertEqual(len(ans), 9, 'there are nine _x00 categories')

    def testAddContent(self):    
        """function that change content"""
        inst = self.createInstance()
        inst.addEntry(inst.nextCategory('d1'), 'Dummy Entry',
                      'A new key word description', 'A401', 'B301')
        self.assertEqual(len(inst.data), TEST_DB_COUNT+1,
                           'confirm the DB is has changed')
        ans = inst.data.search('key', 'dummy')
        self.assertEqual(ans[0]['Category'], 'D100', 'added next entry number')
        
from os import path
print('\nTesting class FindAdex in module:\n',path.abspath(FindAdex.__module__))

if __name__=='__main__':
    unittest.main()
    print('Tests to be added:')
    print('    Save DB')
    print('    The output is also supposed to be in a cetain order')
    
