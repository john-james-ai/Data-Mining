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
from itertools import combinations
from operator import itemgetter
import pandas as pd
from time import time
# --------------------------------------------------------------------------- #
class Apriori:
    """Apriori Algorithm
    
    Implements the Apriori algorithm famously proposed by Agrawal and
    Srikant in their paper 'Fast Algorithms for Mining Association Rules'.

    Parameters
    ----------
    data_filename : str
        the path to the file containing the transaction database to mine.

    frequent_sets_filename : str
        The path where frequent sets are to be stored.

    minsup : float [0,1]
        The minimum relative support for frequent itemsets.

    output_size : bool, default=False
        should itemset size be provided in the output


    Returns
    -------
    frequent_itemsets : list,
        file containing frequent itemsets in the format
            'support:itemset'
        where one itemset per line.
    """

    def __init__(self, data_filename, frequent_sets_filename, minsup=0.1, 
                    output_size=True):
        self._data_filename = data_filename
        self._frequent_sets_filename = frequent_sets_filename
        self._minsup = minsup
        self._output_size = output_size

    def preprocess(self):
        """Loads, maps, and creates the transaction DataFrame in Pandas."""
        


