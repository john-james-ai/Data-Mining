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
#%%
from collections import OrderedDict
# --------------------------------------------------------------------------- #
class IO:
    def __init__(self, infilepath="./data/categories.txt", outfilepath="./data/patterns.txt"):        
        """Performs file input/output as well as itemset normalization."""
        self._infilepath = infilepath
        self._outfilepath = outfilepath

    def read(self):
        """Loads datas data into a transaction database in dictionary format."""        
        d = OrderedDict()        
        with open(self._infilepath, "r") as f:
            for i, line in enumerate(f):                
                d[i] = line.split("\n")[0].split(";")
        return d

    def write(self, X, k=1):
        """Writes i=1:k decoded itemsets to outfilepath as per specification"""
        with open(self._outfilepath, "a") as f:
            for i in range(k):
                for itemset in X[i+1]["itemset_list"]:
                    line = str(itemset.support) + ":"
                    line += ';'.join(itemset.items)
                    line += "\n"
                    f.write(line)
                
#%%
