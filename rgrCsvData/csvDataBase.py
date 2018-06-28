# -*- coding: utf-8 -*-
"""
    Access to csv database
    CsvItem      A line in the file held as a dict with the heading 
                 used as the keys
    CsvDataBase  A list of CsvItems read from a csv file
                 All items that are not under a heading are grouped
                 together into a list using the last heading name.
                 
                                                            rgr01jul17
"""
from __future__ import print_function
import logging
logger = logging.getLogger(__name__)

from collections import OrderedDict
import re

class CsvItem(OrderedDict):
    def __init__(self, keys):
        """Initiate a blank ordered dict with the last item as a list

            keys : list of strings that are the keys"""
        _entry = [(k, '') for k in keys]
        self.length = len(keys)
        super(CsvItem, self).__init__(_entry)
        self[keys[-1]] = []
        
    def read(self, values):
        """Read values into the keys in the order given.  Any missing at the end
           are left blank and any excess are mereged into the last list item

           values : list, any excess white space will be stripped off"""
        logger.debug(values)
        values = [x for x in values if len(x)>0]
        keys = list(self.keys())
        end = keys.pop(-1)
        n = len(keys)
        (fixed, variable) = values[:n], values[n:]
        for key, value in zip(keys, fixed):
            self[key] = value
        self[end] = []
        for v in variable:
            self[end].append(v) 
        return self
    
    def isList(self, key):
        """indicate if the key is the last one, that is always a list"""
        logger.debug('key position '+str(self.keys().index(key)))
        return self.keys().index(key)-self.length==-1
    
    def valueStrf(self, key, width='0'):
        """return the value for the key in the given field width"""
        # longer values are truncated to fit
        # default 0 gives the minimum required width keyStrf
        value = self[key]   # exact key name needed 
        w = len(value) if width=='0' else int(width)
        if w<6:
            # after inserting padding there is nothing left - so KISS
            value = value[:w]
        elif w<len(value):
            padding = ' .'+w%3*'.'+' '
            # this goes wrong if w<6 because w3=0
            w3 = (w - len(padding))/3
            logger.debug('splitting: '+value+' at '+str(w3))
            value = value[:2*w3]+padding+value[-w3:]
        logger.debug('format using: '+'{:'+str(w)+'}')
        return ('{:'+str(w)+'}').format(value)
                
    def write(self):   # no tests set 
        """output in the key_order given by the csv database"""
        output = []
        for key in self.iterkeys():
            _item = self[key]
            if isinstance(_item, list):
                [output.append(x) for x in _item]
            else:
                output.append(_item)
        return output
    
    def output(self, *args):   # no tests set 
        if len(args) == 0:
            args = self.keys()
        max_key = max(len(a) for a in args)
        key_format = '{{:{:n}s}}'.format(max_key + 1)
        ans = []
        for key in args:
            ans.append((key_format+' {:s}').format(key+':', str(self[key])))
        return '\n'.join(ans)

    def pick(self, *fields):     
        """return a list of just the values of fields given in *fields"""
        # exact field names are expected
        return [self[x] for x in fields if x in self.keys()]

    def extract(self, *fields):  
        """return a dict of the fields given in *fields"""
        return {f:self[f] for f in fields}
        
from os import path      
import csv, shutil
from rgrLib.fileUtils import changeExt
      
class CsvDataBase(list):
    def __init__(self, f_name, itemClass=CsvItem):     
        self.field_names = None
        self.itemClass = itemClass
##        self.indexed = None      # the field used to build the index
        self.index = None
        self.time_stamp = None   # fields used to control backup
        # what if filename doesn't exist?
        self.filename = changeExt(f_name, 'csv')
        self.load()

    def __repr__(self):
        """DB can be v big, so simplified repr"""
        return '<class CsvDataBase>'
               
    def load(self):
        self._load(self.filename)
        
    def getFileTimeStamp(self):
        """return the current time stamp of the DB cvs file"""
        return path.getmtime(self.filename)

    def _load(self, f_name):
        """general load to allow other files to be used"""
        logger.debug('loading: \t'+f_name)
        with open(f_name, 'r') as fin:
            self.time_stamp = path.getmtime(f_name)
            reader = csv.reader(fin)
            self.field_names = [x for x in reader.next() if len(x)>0]
            for each in reader:
                _item = self.itemClass(self.field_names)
                self.append(_item.read(each))
        logger.info('loaded '+str(len(self))+' records')
                
    def _save(self, f_name, order_by=None):
        if f_name==self.filename:       # make a back backup 
            _new_time_stamp = path.getmtime(f_name)
            # use a zero value to over-ride this
            if self.time_stamp!=0 and _new_time_stamp>self.time_stamp:
                logger.warning('csv file has changed since it was opened')
                return
            _back_up = changeExt(f_name, 'bak', True)
            shutil.copy(f_name, _back_up)
            logger.info('created back-up: '+_back_up)
        if order_by is not None:
            if self.field_names.count(order_by)>0:
                self.sort(key = lambda x: x[order_by])
            else:
                self.sort(key=order_by)
        try:
            with open(f_name, 'wb') as fout:
                writer = csv.writer(fout)
                writer.writerow(self.field_names)
                for each in self:
                    writer.writerow(each.write())                
                logger.info('saved '+str(len(self))+' records')
        except IOError:
            logger.info('IOError opening '+f_name+' permssion denied')
        # re-stamp the in-memory data
        self.time_stamp = self.getFileTimeStamp()
            
    def save(self, order_by=None):
        """save in the order given, default is by the first field"""
        self._save(self.filename, order_by)
            
    def findKey(self, key, ignore_case=True, first=True):
        """given a text fragment, return an exact field name""" 
        r = re.compile(key, re.IGNORECASE if ignore_case else 0)
        ans = filter(r.match, self.field_names)
        if len(ans)>0 and first:
            return ans[0]
        elif len(ans)>0:
            return ans
        raise KeyError(key +' not in ' + str(self.itemClass))

    def makeIndex(self, key, *fields):
        """save in index all items by key given holding just those fields"""
        self.index = {x[key]:x.extract(*fields) for x in self}

    def isIndexed(self):
        """return whether database has an index"""
        return self.index is not None

    def search(self, key, info, ignore_case=True):
        """regex search the DB for any reference to info in key provided"""
        # keys can be abbreviated, uses a regex search for info
        # returns a list, empty if no match
        if len(self)==0:
            return
        _key = self.findKey(key, first=False)
        if _key is None:
            logger.warning('key: '+key+' not found')
            return []
        key = _key[0]
        r = re.compile(info, re.IGNORECASE if ignore_case else 0)
        # all items are the same so use [0] for test
        if self[0].isList(key):
            # search each item if the field is a list
            return [x for x in self if filter(r.search, x[key])]
        else:
            return [x for x in self if r.search(x[key])]
            
    def _show(self, index, formatted=False, *args):
        if formatted:
            fields = [[a, '0'] if len(a.split(':'))==1 else a.split(':') 
                          for a in args]
            ans = []
            logger.debug('formatter: '+str(fields))
            for f in fields:
                key = self.findKey(f[0])
                ans.append(self[index].valueStrf(key, f[1]))
            print(' '.join(ans))
        else:
            print(self[index].output(*args))
            
    def show(self, start, stop=None, *args):
        """print a list using the range and fileds given in the args"""
        if len(args)==0:
            args = self.field_names
        # extra False for when args=[]
        formatted = max([x.count(':')>0 for x in args], False)
        if stop is None:
            self._show(start, formatted, *args)
        else:
            for i in range(start, stop):
                self._show(i, formatted, *args)
                
def test(f_name):
    logger.info('\tre-testing using' + f_name)
    return CsvDataBase(f_name)

if __name__=='__main__':  
    from sys import stdout
    from time import strftime
    #logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
    logging.basicConfig(stream=stdout)
    logger.level = logging.INFO
    
    logger.info('\tstarting: '+path.basename(__file__)+'\t==='
                 + strftime('%a-%d %H:%M') + ' ===')
    cc = test('../test/CategoriesDB')
