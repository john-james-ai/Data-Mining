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
from itertools import combinations
from operator import itemgetter
import pandas as pd
from time import time

from IO import IO
from preprocessing import AprioriDatafy 
from sklearn.preprocessing import OneHotEncoder, MultiLabelBinarizer
from utils import print_dict
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
        self._db = None     # Database
        self._L_1 = None    # L_1-itemsets
        self._Lk = None    # Large k-itemsets
        self._Ck = None    # Candidate k-itemsets
        self._frequent_itemsets = pd.DataFrame()  # all frequent itemsets

    def preprocess(self):
        """Loads, maps, and creates the transaction database as a Pandas DataFrame."""    
        datafy = AprioriDatafy(self._infilepath, self._outfilepath, self._start_idx) 
        self._db = datafy.fit_transform()
        self._minsup = self._minrelsup * self._db.shape[0]        

    def gen_l1_itemsets(self):
        """Creates L1 large itemsets."""
        # Extract rows with at least one item
        subset = self._db[self._db.sum(axis=1)>0]        
        # Get the columns names containing frequent 1-itemsets
        items = subset.columns[(subset.sum(axis=0) >= self._minsup)].values
        # Count support by summing axis=0
        support = subset.iloc[:,items-self._start_idx].sum(axis=0)
        # Format and return
        self._L_1 = pd.DataFrame(
            {'k':1, 'items': items, "support": support.values})
        self._L_1.to_string(index=False)        

    def join(self, k, Lk_1):
        """Joins Lk-1 itemset with itself to get all combinations of itemsets""" 
        return list(combinations(Lk_1['items'].values, k))

    def prune(self, Ck):
        """Deletes candidates whos subsets are not frequent."""
        mask = []
        for c in Ck:
            col_idx = [col-self._start_idx for col in c]
            items = self._db.iloc[:,list(col_idx)]
            mask.append(sum(items.all(axis=1)) >= self._minsup)
        Ck = [b for a,b in zip(mask, Ck) if a]
        return Ck
            

    def get_candidates(self, k):
        """Generates candidates Ck."""
        # Obtain l_k-1 from frequent itemsets.
        Lk_1 = self._frequent_itemsets[self._frequent_itemsets.k == k-1]
        print("\nLk_prev")
        print(Lk_1)
        # Reduce transaction database to those itemsets >= k
        self._db = self._db[self._db.sum(axis=1) >= k]
        print("\nDatabase after")
        print(self._db)
        # Join step: Get the combinations from lk-1
        print("\nCk")
        Ck = self.join(k, Lk_1)
        print(Ck)
        # Prune step: delete candidates that are not frequent
        Lk = self.prune(Ck)
        self._frequent_itemsets.append(Lk)
        print(Lk)
        
        return Lk


    def mine(self):
        self.preprocess()
        self.gen_l1_itemsets()
        self._Lk = self._L_1
        self._frequent_itemsets = self._Lk 
        self.get_candidates(2)
        self._frequent_itemsets = self._Lk 
        self.get_candidates(3)
        self._frequent_itemsets = self._Lk 
        print(self._frequent_itemsets)

        # while (self._L_k.shape[0] > 0):

        #     for size in range(2, len(self._L_1) + 1):
        #         self.get_candidates(size)
        #         if self._L_k.shape[0] == 0: 
        #             break


if __name__ == '__main__':
    infilepath = "./data/figure3.txt"
    outfilepath = "./data/patterns.txt"

    apriori = Apriori(infilepath, outfilepath, 0.5, 1)
    apriori.mine()
    

#%%
