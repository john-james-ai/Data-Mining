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
class Database:
    def __init__(self, transactions):
        self._transactions = transactions
    
    def get_support(self, candidate):


class DataBaseFactory:
    def __init__(self, filename):        
        "Creates a Database Object
        self._filename = filename
        self._filehandler = None
        self._Database = None
        self._lines = []
        self._trans_list = []        
        self._trans_id = 0
        self._item_id = 0
        self._item_seq = 0
        self._transactions = pd.DataFrame()
    
    def read(self):
        """Adds a parent to the node, indexed by the text of the parent node."""
        self._filehandler = open(self._filename,'r')
        self._lines = self._filehandler.readlines()       

    def parse(self):
        """ Parses and loads data into list of dictionaries.""" 
        for line in self._lines:
            items = line.split(";")
            self._item_seq = 0
            for item in items:
                d = {'trans_id': self._trans_id, 
                     'item': self._item,
                     'is_frequent': False}
                self._trans_list.append(d)
            self._trans_id += 1

    def get_database(self):
        """Sorts each transaction by item."""
        self._sorted_transactions = sorted(self._trans_list, key = lambda t: (t['trans_id'], t['item']))
        self._database = Database(self._sorted_transactions)
        return self._database

