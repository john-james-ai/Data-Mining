# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Mining                                                       #
# File    : \apriori.py                                                       #
# Python  : 3.9.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : nov8.ai                                                           #
# Email   : john.james@nov8.ai                                                #
# URL     : https://github.com/john-james-sf/Data-Mining/                     #
# --------------------------------------------------------------------------- #
# Created       : Thursday, February 11th 2021, 8:44:58 am                    #
# Last Modified : Wednesday, February 17th 2021, 11:29:15 am                  #
# Modified By   : John James (john.james@nov8.ai)                             #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2021 nov8.ai                                                  #
# =========================================================================== #
from collections import OrderedDict
# --------------------------------------------------------------------------- #
class IO:
    def __init__(self, transaction_filename, _frequent_item_filename):        
        "Performs file input/output as well as itemset normalization.
        self._transaction_filename = None
        self._frequent_item_filename = None
        self._item_map = OrderedDict()
        self._transactions = pd.DataFrame()
            
    def read(self):
        """Reads the transaction database file."""
        self._items = pd.read_csv(self._transaction_filename, sep=";", header=None)
        with open(self._transaction_filename,'r') as f:
            itemlist = sorted(item for line in f for item in line.split(";"))
        
        self._item_map = dict([(item,n+1) for n,item in enumerate(sorted(set(itemlist)))])


        lines = filehandler.readlines()       

            

    def load(self, transaction_filename):
        """Adds a parent to the node, indexed by the text of the parent node."""
        self._read()
        self._parse()
        self._normalize()
        self._filehandler = open(self._filename,'r')
        self._lines = self._filehandler.readlines()       

    def parse(self):
        """ Parses and loads data into list of dictionaries.""" 
        for line in self._lines:
            items = line.split(";")
            self._item_seq = 0
            for item in items:
                d = {'tid': self._trans_id, 
                     'item': self._item,
                     'is_frequent': False}
                self._tlist.append(d)
            self._trans_id += 1

    def get_database(self, n=None):
        """Sorts each transaction by item."""
        self._sorted_tlist = sorted(self._tlist, key = lambda t: (t['trans_id'], t['item']))
        self._transactions = pd.DataFrame(self._sorted_tlist)
        if n:
            self._transactions.sample(n=n)
        self._database = Database(self._transactions)
        return self._database

