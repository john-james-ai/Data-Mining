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
import pandas as pd
from time import time

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

    def __init__(self, infilepath, outfilepath, minrelsup=0.01, start_idx=0):
        self._infilepath = infilepath
        self._outfilepath = outfilepath
        self._minrelsup = minrelsup
        self._start_idx = start_idx
        self._minsup = 0
        self._db = None    
        self.L = Itemsets()  # all frequent itemsets
        self.Lk = Itemsets() # all k-itemsets that are frequent 
        
    def preprocess(self):
        """Loads, maps, and creates the transaction database as a Pandas DataFrame."""    
        datafy = AprioriDatafy(self._infilepath, self._outfilepath, self._start_idx) 
        self._db = datafy.fit_transform()
        self._minsup = self._minrelsup * self._db.shape[0]        

    def gen_l1_itemsets(self):
        """Creates L1 large itemsets as list of dictionaries."""
        # Extract rows with at least one item
        subset = self._db[self._db.sum(axis=1)>0]        
        # Get the columns names containing frequent 1-itemsets
        items = subset.columns[(subset.sum(axis=0) >= self._minsup)].values
        # Count support by summing axis=0
        support = subset.iloc[:,items-self._start_idx].sum(axis=0)
        # Add k1 itemsets to L and Lk itemset objects
        for item,s in zip(items, support):
            d = {"k": 1, "itemset": item, "support": s}
            self._L.add_itemset(d)
            self._Lk.add_itemset(d)
        

    def get_frequent(self, k, Ck):
        """Prunes infrequent itemsets and returns new frequent itemsets."""
        Lk = pd.DataFrame()
        for c in Ck:
            col_idx = [col-self._start_idx for col in c]
            subset = self._db.iloc[:,list(col_idx)]
            support = subset[subset.sum(axis=1) == k].shape[0]
            if support >= self._minsup:
                print(f"adding {c} to Lk")
                df = pd.DataFrame({"k":k, "support": support}, index=[k])
                df["itemset"] = c
                Lk = Lk.append(pd.DataFrame(d))                
        return Lk
            

    def get_candidates(self, k, Lk_prev):
        """Generates candidates Ck."""        

        # Join step: Get the combinations from lk-1
        print("\nLk_prev itemsets")
        itemsets = sorted(set(Lk_prev['itemsets'].values))
        Ck = map(list, combinations(itemsets, k))
        print(f"Initial set of k={k} candidates")
        print(Ck)        
        # Prune step: Not as per Argawal. Rather, removing duplicate items from itemsets
        Ck = [item for item in Ck if len(set(item)) == len(item)]
        print(f"Returning the following k={k} candidates")
        print(Ck)
        return Ck


    def mine(self):                        
        
        self.preprocess()

        self.gen_l1_itemsets()
        self.L.print()
        k = 2
        while (len(Lk_prev) != 0):
            Ck = self.get_candidates(k, Lk_prev)
            Lk = self.get_frequent(k, Ck)
            frequent_itemsets = frequent_itemsets.append(Lk)
            Lk_prev = Lk
            k += 1
        print(frequent_itemsets)
        #self.save_itemsets(frequent_itemsets)


if __name__ == '__main__':
    infilepath = "./data/figure3.txt"
    outfilepath = "./data/patterns.txt"

    apriori = Apriori(infilepath=infilepath, outfilepath=outfilepath, minrelsup=0.5, start_idx=1)
    apriori.mine()
    

#%%
