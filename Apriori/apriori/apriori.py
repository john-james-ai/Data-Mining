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
# Created       : Thursday, February 18th 2021, 2:28:56 am                    #
# Last Modified : Thursday, February 18th 2021, 2:28:56 am                    #
# Modified By   : John James (john.james@nov8.ai)                             #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2021 nov8.ai                                                  #
# =========================================================================== #
#%%
from collections import OrderedDict
from itertools import combinations
from operator import itemgetter
import numpy as np
import pandas as pd
import time

from IO import IO
from itemsets import Itemsets
from preprocessing import AprioriDatafy 
# --------------------------------------------------------------------------- #
class Apriori:
    """Apriori Algorithm
    
    Implements the Apriori algorithm proposed by Agrawal and Srikant in their paper 
    'Fast Algorithms for Mining Association Rules'.

    Parameters
    ----------
    infilepath : str
        the path to the file containing the transaction database to mine.

    outfilepath : str
        The path to which frequent itemsets are to be stored

    minsup : float [0,1]
        The minimum relative support for frequent itemsets.

    Returns
    -------
    frequent_itemsets : file,
        file containing frequent itemsets in the format
            'support:[itemset]'
        with one itemset per line.
    """

    def __init__(self, infilepath, outfilepath1, outfilepath2, minrelsup=0.01):
        self._infilepath = infilepath
        self._outfilepath1 = outfilepath1
        self._outfilepath2 = outfilepath2
        self._minrelsup = minrelsup         # Relative minimum support
        self._minsup = 0                    # Absolute minimum support        
        self._itemset_id = 0                # Itemset sequence number
        self._L = Itemsets()                # all frequent itemsets
        self._Lk = Itemsets()               # all k-itemsets that are frequent 
        self._complete = False              # True when all frequent itemsets mined.
        self._datafy = None                 # Object responsible for reading and writing data
        self._io = None                     # Object responsible for file IO     
        self._start_time = None
        self._end_time = None
        
    def _start(self):
        """Loads, maps, and creates the transaction database as a Pandas DataFrame."""    
        self._start_time = time.time()
        self._io = IO()
        db = self._io.read(self._infilepath)
        self._datafy = AprioriDatafy() 
        self._db = self._datafy.fit_transform(db)
        self._minsup = self._minrelsup * self._db.shape[0]        

    def _gen_L1_itemsets(self):
        """Creates L1 large itemsets as list of dictionaries."""
        # Get 1-itemsets by summing over rows >= minsup
        items = self._db.loc[:,self._db.sum(axis=0)>=self._minsup].columns    
        # Count support by summing axis=0
        support = self._db.iloc[:,items].sum(axis=0)
        # Add k1 itemsets to L and Lk itemset objects
        for item,s in zip(items, support):            
            d = {"k": 1, "id": self._itemset_id, "itemset": item, "support": s}
            self._L.add_itemset(d)
            self._Lk.add_itemset(d)
            self._itemset_id += 1
        

    def _set_frequent(self, k, Ck):
        """Prunes infrequent itemsets and returns new frequent itemsets."""
        Lk = pd.DataFrame()
        for c in Ck:
            col_idx = [col for col in c]
            subset = self._db.iloc[:,list(col_idx)]
            support = subset[subset.sum(axis=1) >= k].shape[0]
            if support >= self._minsup:
                d = {"k": k, "id": self._itemset_id, "itemset": c, "support": support}
                self._L.add_itemset(d)
                self._Lk.add_itemset(d)     
                self._itemset_id += 1


    def _extract_items(self, k):
        """Extracts individual items from lk-1 and dedups."""           
        items = []
        itemsets = sorted(list(self._Lk.get_itemsets(k-1)))        
        if k > 2: 
            a = [x for l in itemsets for x in l]
            [items.append(x) for x in a if x not in items]
        else:
            [items.append(x) for x in itemsets if x not in items]        
        return items                

    def _get_candidates(self, k):
        """Generates candidates Ck."""        
        # Extract step: Get all items from lk-1 itemsets
        items = self._extract_items(k)
        # Join step: Get the combinations from lk-1        
        Ck = list(combinations(items, k)) 
        # if Ck size is 0, we're done.
        if len(Ck) == 0: self._complete = True
        else:
            # Re-sort after converting to list
            Ck = sorted(Ck)
            Ck = [sorted(item) for item in Ck]        
            # Prune step: Remove itemsets whose k-1 items are not frequent 
            Ck = list(self._Lk.prune_candidates(k,Ck))
            if len(Ck) == 0: self._complete = True            
        return Ck

    def _finish(self):
        """Write L, all frequent itemsets, to file."""
        L1, Lk = self._datafy.inverse_transform(self._L)
        self._io.write(L1, self._outfilepath1)        
        self._io.write(Lk, self._outfilepath2)       
        self._end_time = time.time()
        e = round(self._end_time - self._start_time,3)
        self._L.summary()
        print(f"Elapsed time: {e} seconds")
        

    def mine(self):                        
        
        self._start()

        self._gen_L1_itemsets()
        self._L.print()
        k = 2
        while (self._Lk.total_itemsets != 0 and 
               not self._complete):
            Ck = self._get_candidates(k)
            
            if self._complete: break
            
            self._set_frequent(k, Ck)            
            k += 1        
        self._finish()


if __name__ == '__main__':
    infilepath = "./data/categories.txt"
    outfilepath1 = "./data/F1/patterns.txt"
    outfilepath2 = "./data/Fn/patterns.txt"

    apriori = Apriori(infilepath=infilepath, outfilepath1=outfilepath1, 
                      outfilepath2=outfilepath2, minrelsup=0.01)
    apriori.mine()
    

#%%
