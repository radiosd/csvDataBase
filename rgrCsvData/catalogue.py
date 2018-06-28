# -*- coding: utf-8 -*-
"""
    Encapsulation of the MasterCatalogue for the library of papers 
    Record      A CsvItem for every entry in the Catalogue
    
    Catalogue   A CsvDataBase of all the catalogue items in the DB    

                                                               rgr07jly17
"""
import logging
logger = logging.getLogger(__name__)

from csvDataBase import CsvItem        
REQUIRED_FIELDS = ['Category','Title','Journal','Author', 'Descrition']
OPTIONAL_FIELDS = ['Category', 'Paper']
ALL_FIELDS = REQUIRED_FIELDS + OPTIONAL_FIELDS

class Reference(CsvItem): pass

import re

from csvDataBase import CsvDataBase            
class Catalogue(object):
    def __init__(self, filename, itemClass=Reference):
        self.data = CsvDataBase(filename, itemClass)
        self.criteria()  # the default fields used for search pattern

    def __len__(self):
        return len(self.data)

#     this is more appropriate in the CsvDataBase class
##    def newItem(self):
##        """return a new blank item for the database"""
##        if len(self)==0:
##            raise ValueError('database is empty')
##        else:
##            return self.data.itemClass(self.data.field_names)

    def save(self, filename=None):
        """save the DB to the filename given, None=original name"""
        if filenmane is None:
            filename = self.data.filename
        # save the data list using an order derived from the paper number
        # group by 100, 200 etc then first letter and the rest
        order = lambda x: x['Paper'][1]+x['Paper'][0]+x['Paper'][2:]
        self.data._save(filename, order)
        
    def findJob(self, job):
        """return the data record for the job number given"""
        xx = self.data.search('Tags', job)
        if len(xx)!=0:
            return xx[0]
        else:
            return None
    
    def listJobs(self):
        """return a sorted list of all records with a job tag"""
        xx = self.data.search('Tags', 'J[0|1|2]')
        yy = [x['Tags'][-1] for x in xx]
        yy.sort()
        return yy
    
    def fetchJobs(self):
        jj = self.data.search('Tags', 'J[0|1|2]')
        # return having removed any trailling ? on the tag
        return {j['Tags'][-1].split('?')[0]:j for j in jj}
    
    def listNewEntries(self):
        """pick out items with a job tag"""
        return [x for x in self.data if x.hasJobTag()]
        
##    def search(self, field, text, index=True):
##        field = field.title()
##        if ALL_FIELDS.count(field)>0:
##            ans = self.data.search(field, text)        
##            if not index:
##                return ans
##            return [self.data.index(x) for x in ans]
##        else:
##            print 'invalid key for underlying data:', field
    
    def criteria(self, case_sensitive=False, whole_words=False):
        self.whole_words = whole_words
        self.case_sensitive = case_sensitive

    def createPattern(self, text):
        """return the regex pattern for the search text given"""
        # for now vey simple, just AND all
        items = ['(?=.*'+x+')' for x in text]
        return ''.join(items)

    def _find(self, pattern, *args):
        ans = []
        for item in self.data:
            # each one is a CsvItem, field abbreviations are not allowed
            text_to_search = ' '.join(item.pick(*args))
            if pattern.search(text_to_search):
                ans.append(item)
        return ans
        
    def find(self, text, *args):
        """return all records with text in any one of the args fields given"""
        # abreviated arg names are expanded
        if len(args)==0:
            raise TypeError('find() requires at least 1 args value')
        # expand args to full filed names
        args = [self.data.findKey(x) for x in args]
        # create the regex pattern
        # for now just AND each item
        case = re.IGNORECASE if not self.case_sensitive else 0
        # list items using white space while stripping any excess
        if isinstance(text, str):
            text = (text,)
        match = self.createPattern(text)
        pattern = re.compile(match, flags=case)
        ans = []
        for item in self.data:
            # each one is a CsvItem, field abbreviations already expanded
            text_to_search = ' '.join(item.pick(*args))
            if pattern.search(text_to_search):
                ans.append(item)
        return ans
    
    def tagSearch(self, tag):
        return self.search('Tags', tag)
    
##    def indexBy(self, key):
##        """create a dict of all entries by the key given"""
##        if len(self.data)==0 and not self.data[0].has_key(key):
##            return
##        ans = {}
##        for item in self.data:
##            _key = item[key]
##            if ans.has_key(_key):
##                ans[_key].append(item)
##            else:
##                ans[_key] = [item,]
##        return ans
            
def main(f_name):
    logging.debug('main in Catalog')
    return Catalogue(f_name, Reference)

if __name__=='__main__':  
    from os import path, sys
    from time import strftime
    logging.basicConfig(stream=sys.stdout)
    logger.level = logging.DEBUG       # change for interactive level
    logger.info('\tstarting: '+path.basename(__file__)+'\t==='
                 + strftime('%a-%d %H:%M') + ' ===')
    #PATH = r'R:\NAS\PdfLibrary'
    PATH = path.join('..', 'test')
    DB_FILE = 'PapersDB'
    mc = main(path.join(PATH, DB_FILE))
    #fad.data._check()
    #print mc.data[0].output()
    def qq(text, show, *fields):
        xx = mc.find(text, *fields)
        print('found:', len(xx))
        if show:
            for x in xx:
                print(x.output(*fields))
        return xx

    ff = ('Author', 'Title', 'Journal')
    text = ' '.join(mc.data[1].pick(*ff))
