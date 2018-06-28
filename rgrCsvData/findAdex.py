# -*- coding: utf-8 -*-
"""
    Encapsulation of the FindAdex idea for categorising papers 
    Category   A CsvItem for every entry in the FinadAdex
    
    FindAdex   A CsvDataBase of all the category items in the DB    

                                                               rgr03Jul17
"""
import logging
logger = logging.getLogger(__name__)
logger.level = logging.INFO

from csvDataBase import CsvItem        
REQUIRED_FIELDS = ['Category','Key Words', 'Description']
OPTIONAL_FIELD = 'See Also'
ALL_FIELDS = REQUIRED_FIELDS + [OPTIONAL_FIELD,]

class Category(CsvItem):   # to replace CatEntry
    """the items to be held in the data base"""
        
    def addFields(self, *values):
        """fill in the minimum required number of fields for the Category"""
        if len(values)==len(REQUIRED_FIELDS):
            for k, v in zip(REQUIRED_FIELDS, values):
                self[k] = v
        else:
            raise ValueError('insufficient values for the required fields')
    
    def makeValidTag(self, tag):
        return tag.upper()
        
    def isValidTag(self, value):
        return len(value)==4 and value[0].isalpha() and value[1:].isdigit()
        
from csvDataBase import CsvDataBase
class FindAdexError(Exception):
    pass

class FindAdex(object):
    """encapsulation of the FindAdex index of the various categories"""
    def __init__(self, filename, itemClass=Category):
        self.itemClass = itemClass
        self.data = CsvDataBase(filename, itemClass)
        
    def save(self):
        # save the data list in the category and number order
        order = lambda x: x['Category'][1]+x['Category'][0]+x['Category'][2:]
        self.data.save(order)
        
    def hasCategory(self, code):
        """return whether or not a category has been defined"""
        return len(self.listCategories(code.upper()))>0
    
    def nextCategory(self, code):
        """return the next numberic code for the category given"""
        ll = [x['Category'] for x in self.data.search('Category', code[:2])]
        ss = [99] if len(ll)==0 else [int(x[1:]) for x in ll]
        return code[0].upper() + str(max(ss)+1)
        
    def listCategories(self, mask):
        # s simple linear search for now
        return self.data.search('Category', mask)   
        
    def addEntry(self, category, key_words, description, *see_also):
        """add a complete entry to FindAdex, see_also is an optional list"""
        if self.hasCategory(category):
            raise FindAdexError('duplicate entry: ' + category)
        _entry = self.itemClass(ALL_FIELDS)
        category = _entry.makeValidTag(category)
        if category[2:]=='00':
            category = self.nextCategory(category)
            logger.debug('next category: ' + category)
        if _entry.isValidTag(category):
            _entry.addFields(category, key_words, description)
            for sa in see_also:   
                sa = sa.upper() # _entry.makeValidTag(sa)    # this just makes it UC
                if _entry.isValidTag(sa):       # check correct format
                    _entry[OPTIONAL_FIELD].append(sa)
                else:
                    raise FindAdexError('invalid Tag: ' + sa)
            self.data.append(_entry)
        else:
            # not the best option but ok for now
            raise FindAdexError('invalid category: ' + category)

    def fail(self):
        # just for testing
        raise FindAdexError('a deliberate fail')
        
def xxx(fad):
    try:
        fad.fail()
    except FindAdexError, error:
        print error
        
def main(f_name):
    logging.debug('main in FindAdex')
    return FindAdex(f_name, Category)

if __name__=='__main__':  
    from os import path
    from sys import stdout
    from time import strftime
    #logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
    logging.basicConfig(stream=stdout)
    logger.level=logging.DEBUG
    logger.info('\tstarting: '+path.basename(__file__)+'\t==='
                 + strftime('%a-%d %H:%M') + ' ===')
    # Library DB
    #PATH = r'R:\NAS\PdfLibrary'
    PATH = '.'
    CAT_FILE = 'CategoriesTest'
    # local test DB
    #PATH = ''
    #CAT_FILE = 'CategoriesTest'

    fad = main(path.join(PATH, CAT_FILE))
    #fad.data._check()
    print fad.data[0].output()
