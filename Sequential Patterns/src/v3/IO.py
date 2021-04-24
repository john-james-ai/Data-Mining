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
# Last Modified : Saturday, April 24th 2021, 12:32:04 am                      #
# Modified By   : John James (jtjames2@illinois.edu)                          #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2021 nov8.ai                                                  #
# =========================================================================== #
#%%
import os
from collections import OrderedDict
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

# --------------------------------------------------------------------------- #
class IO:
    def __init__(self):        
        """Performs file input/output as well as itemset normalization."""
        self._integize = Integize()

    def read(self, filepath):
        """Loads datas into a transaction database in dictionary format."""   
        reviews = []             
        with open(filepath, "r") as f:
            reviews = [line.split() for line in f]                    
        # Convert strings to integers
        X = self._integize.fit(reviews).transform(reviews)
        return X
        
    
    def write(self, X, filepath):
        """Writes decoded itemsets to filepath as per specification"""
        # Convert integers back to strings.
        X = self._integize.inverse_transform(X)
        if  os.path.exists(filepath):
            os.remove(filepath)
        with open(filepath, "a") as f:       
            for k, sequences in X.items():
                for sequence in sequences:
                    line = str(sequence["support"]) + ":" + str(';'.join(sequence["sequence"])) + "\n"                    
                    f.write(line)

# --------------------------------------------------------------------------- #
class Integize(BaseEstimator, TransformerMixin):
    """Converts strings to ints and back."""
    def __init__(self):
        self._to_int = {}
        self._to_string = {}

    def fit(self, X,y=None):
        X_flat = [word for item in X for word in item]
        X_unique = list(dict.fromkeys(X_flat))
        for i, word in enumerate(X_unique):
            self._to_int[word] = i
            self._to_string[i] = word        
        return self

    def transform(self, X):
        """Converts words in a transaction database to integers.
        
        Parameters
        ----------
        X: 
        
        """
        result = []
        for review in X:
            result.append([self._to_int[word] for word in review])
        return result

    def inverse_transform(self, X):
        """Converts sequences (dict of nested lists) of integers to strings."""
        result = {}
        for k, sequences in X.items():
            result[k] = []
            for sequence in sequences:
                string_sequence = [self._to_string[i] for i in sequence["sequence"]]
                d = {"k": k, "sequence": string_sequence, "support": sequence["support"]}                
                result[k].append(d)
        return result

                
#%%
