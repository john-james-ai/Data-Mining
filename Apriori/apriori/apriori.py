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
from preprocessing import Encoder, DictEncoder 
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

    def __init__(self, infilepath, outfilepath, minrelsup=0.01):
        self._infilepath = infilepath
        self._outfilepath = outfilepath
        self._minrelsup = minrelsup
        self._minsup = 0
        self._db = None
        self._frequent_itemsets = pd.DataFrame()

    def preprocess(self):
        """Loads, maps, and creates the transaction database as a Pandas DataFrame."""                
        io = IO(self._infilepath, self._outfilepath)
        db = io.read()
        # Encode the items to integers
        encoder = Encoder()
        db = encoder.fit_transform(db)        
        db = pd.Series(db)
        # Create the one-hot dataframe using sklearn's MultiLabelBinarizer
        mlb = MultiLabelBinarizer()
        self._db = pd.DataFrame(mlb.fit_transform(db),
                   columns=mlb.classes_,
                   index=db.index)
        self._minsup = self._minrelsup * self._db.shape[0]
        return self._db

    def gen_l1_itemsets(self):
        """Creates L1 large itemsets."""
        # items = self._db.apply(pd.value_counts).sum(axis=0)\
        #     .where(lambda value: value >= self._minsup).dropna()

        items = pd.Series(self._db[self._db.sum(axis=0)>=self._minsup].columns)
        print("\nItems")
        print(items)

        self._frequent_itemsets = pd.DataFrame(
            {'k':1, 'items': items.index.astype(int), "support": items.values})

        return self._frequent_itemsets.to_string(index=False)


if __name__ == '__main__':
    infilepath = "./data/figure3.txt"
    outfilepath = "./data/patterns.txt"

    apriori = Apriori(infilepath, outfilepath, 0.5)
    df = apriori.preprocess()
    print(df)
    l1 = apriori.gen_l1_itemsets()
    print(l1)
    #print_dict(l1,10)

#%%
