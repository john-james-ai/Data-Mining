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
import os
from collections import OrderedDict
# --------------------------------------------------------------------------- #
class IO:
    def __init__(self):        
        """Performs file input/output as well as itemset normalization."""
        pass

    def read(self, filepath):
        """Loads datas data into a transaction database in dictionary format."""        
        d = OrderedDict()        
        with open(filepath, "r") as f:
            for i, line in enumerate(f):                
                d[i] = line.split("\n")[0].split(";")
        return d
    
    def write(self, X, filepath):
        """Writes decoded itemsets to outfilepath as per specification"""
        if  os.path.exists(filepath):
            os.remove(filepath)
        with open(filepath, "a") as f:            
            for i in range(len(X)):
                if isinstance(X[i]["itemset"], list):
                    line = str(X[i]["support"]) + ":" + str(';'.join(X[i]["itemset"])) + "\n"                    
                else:
                    line = str(X[i]["support"]) + ":" + str(X[i]["itemset"]) + "\n"    
                f.write(line)



                
#%%
