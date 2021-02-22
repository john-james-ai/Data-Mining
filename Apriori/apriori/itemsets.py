# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Mining                                                       #
# File    : \itemset.py                                                       #
# Python  : 3.9.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : nov8.ai                                                           #
# Email   : john.james@nov8.ai                                                #
# URL     : https://github.com/john-james-sf/Data-Mining/                     #
# --------------------------------------------------------------------------- #
# Created       : Monday, February 22nd 2021, 11:19:21 am                     #
# Last Modified : Monday, February 22nd 2021, 11:19:33 am                     #
# Modified By   : John James (john.james@nov8.ai)                             #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2021 nov8.ai                                                  #
# =========================================================================== #
#%%
from collections import OrderedDict
import numpy as np
import pandas as pd
# --------------------------------------------------------------------------- #
class Itemsets:
    def __init__(self):
        self._itemsets = OrderedDict()
        self._itemset_counts = OrderedDict()
        self.total_itemsets = 0        

    def get_itemsets(self, k=None):
        """Returns list of k-itemsets if k is provided, otherwise, all itemsets."""
        if k:
            return self._itemsets[k]
        else:
            return self._itemsets


    def add_itemset(self, itemset):
        """Adds itemset to collection and updates counts."""
        #Get k. If k exists, append to list of itemsets. Otherwise, create list
        if itemset["k"] in self._itemsets.keys():
            # Append itemset to list
            self._itemsets[itemset["k"]].append(itemset)            
            self._itemset_counts[itemset["k"]] += 1
            self.total_itemsets += 1
        else:
            itemsets = []
            itemsets.append(itemset)            
            self._itemsets[itemset["k"]] = itemsets
            self._itemset_counts[itemset["k"]] = 1
            self.total_itemsets = 1

    def add_itemset_list(self, itemsets):
        """Add a list of itemsets. Used for L1 itemsets."""
        for itemset in itemsets():
            self.add(itemset)

    def _print_itemsets(self, k):
        """Prints the k-ary itemsets in tabular format."""
        d = self._itemsets[k]
        df = pd.DataFrame(d)
        h1 = "="*40        
        h2 = "_"*40
        print("\n")
        print(h1)
        print(f"              {k}-Itemsets")
        print(h2)
        print(df.to_string(index=False))           

    def print(self, k=None):
        if k:
            self._print_itemsets(k)
        else:
            for k_ in self._itemsets.keys():
                self._print_itemsets(k_)


    def summary(self):
        """Summarizes the counts of itemsets by size."""
        h1 = "="*40        
        h2 = "_"*40
        print("\n")
        print(h1)
        print(f"        Itemset Counts by Size")
        print(h2)        
        d = {"k": [k for k in self._itemset_counts.keys()], 
             "Num": [v for v in self._itemset_counts.values()]}
        df = pd.DataFrame(d)
        print(df)

        
if __name__ == '__main__':
    itemsets = Itemsets()
    for i in range(5):
        n_itemsets = np.random.randint(1,10,1)            
        for j in range(n_itemsets[0]):
            iset = {}
            iset["k"] = i
            iset["itemset"] = np.random.randint(1,100, i)
            iset["support"] = np.random.randint(1,100,1)
            itemsets.add_itemset(iset)
    itemsets.print()
    itemsets.summary()
#%%
            


