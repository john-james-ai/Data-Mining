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
# Last Modified : Monday, April 19th 2021, 1:51:19 pm                         #
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
class DB:
    """ The transaction database."""
    def __init__(self, infile, outfile, trie):        
        self._infile = infile
        self._outfile = outfile
        self.db = None
        self.trie = trie

    def read(self):
        """Reads the transaction database from file."""                
        with open(self._infile, "r") as f:
             self.db = [line.split() for line in f]        
    
    def write(self, X, filepath):
        """Writes sequences and support to outfile as per specification"""
        if  os.path.exists(self._outfile):
            os.remove(self._outfile)
        with open(self._outfile, "a") as f:       
            for k, sequences in X.items():
                for sequence in sequences:
                    line = str(sequence["support"]) + ":" + str(';'.join(sequence["sequence"])) + "\n"                    
                    f.write(line)

    def load(self):
        """Loads database into the trie."""
        for line in self.db:
            for word in line:
                self.trie.insert(word)


                
#%%
