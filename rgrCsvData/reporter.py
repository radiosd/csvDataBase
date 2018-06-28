# -*- coding: utf-8 -*-
"""
    Encapsulation of a search and report class for a CsvDataBase

                                                           rgr06jun18
"""

import re
class Reporter(object):
    def __init__(self, target):
        self.data = target.data
        self.fields = []      # fields for the search
        self.criteria()
        self.report = []      # holder for search results

    def criteria(self, case_sensitive=False, whole_words=False):
        """set the default search criteria"""
        self.whole_words = whole_words
        self.case_sensitive = case_sensitive

##    def clear(self):
##        """empty the internal report"""
##        self.report = []

    def properFields(self, args, require_match=False, warning=False):
        """expand field names to full values"""
        ans = []
        if len(self.data)>0:
            inst = self.data[0]
            ans = [inst.findKey(x) for x in args if len(inst.findKey(x))]
            if warning and len(args)-len(ans)>0:
                print 'warning some field names not found'
        return ans
 
    def searchFields(self, *args):
        """set the fields to be used in the search"""
        self.fields = self.properFields(args)

    def search(self, text, append=False):
        """search the target for the text given"""
        case = re.IGNORECASE if not self.case_sensitive else 0
        match = r'\b' + text + r'\b' \
                if self.whole_words else text
        pattern = re.compile(match, flags=case)
        ans = self.report if append else []
        for item in self.data:
            # each one is a CsvItem, field abbreviations are not allowed
            if filter(pattern.search, [item[k] for k in self.fields]):
                ans.append(item)
        self.report = ans

    def output(self, *args):
        """produce a list of lines from the report using the fields given"""
        # should this be a dict indexed by the paper id
        ans = []
        if len(self.data)>0:
            inst = self.data[0]
            out_fields = self.properFields(args)
            for item in self.report:
                entry = []
                for key in out_fields:
                    entry.append(item[key])
                ans.append(entry)
        return ans

if __name__=='__main__':
    pass
