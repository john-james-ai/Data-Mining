# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Mining                                                       #
# File    : \sequence.py                                                       #
# Python  : 3.9.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : nov8.ai                                                           #
# Email   : john.james@nov8.ai                                                #
# URL     : https://github.com/john-james-sf/Data-Mining/                     #
# --------------------------------------------------------------------------- #
# Created       : Monday, February 22nd 2021, 11:19:21 am                     #
# Last Modified : Tuesday, April 20th 2021, 9:28:17 pm                        #
# Modified By   : John James (jtjames2@illinois.edu)                          #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2021 nov8.ai                                                  #
# =========================================================================== #
#%%
from collections import OrderedDict
from itertools import combinations
import numpy as np
import pandas as pd
import time
# --------------------------------------------------------------------------- #
class Sequences:
    def __init__(self):
        self._sequences = {}
        self._last_checkpoint = time.time()
        self.total_sequences = 0        

    def get_sequences(self, k):
        """Returns a list of sequences of size k."""        
        return self._sequences[k]

    def get_sequence_db(self, k=None):
        """This returns the entire sequence object or the k sequences"""
        return self._sequences

    def add_sequences(self, k, sequences):        
        self._sequences[k] = sequences

    def _print_sequences(self, k):
        """Prints the k-ary sequences in tabular format."""
        sequences = []
        supports = []
        for sequence, support in self._sequences[k].items():
            sequences.append(sequence)
            supports.append(support)
        d = {"Support": supports, "Sequence": sequences}
        df = pd.DataFrame(d)           
        h1 = "="*40        
        h2 = "_"*40
        print("\n")
        print(h1)
        print(f"{k}-Sequences")
        print(h2)
        print(df.to_string(index=False))           

    def print(self, k=None):
        if k:
            self._print_sequences(k)
        else:
            for k_ in self._sequences.keys():
                self._print_sequences(k_)

    def print_status(self, k):        
        if k in self._sequence_counts.keys():
            now = time.time()
            elapsed = round(now - self._last_checkpoint,3)
            count = self._sequence_counts[k]
            print(f"    k:{k}   # Sequences: {count}   Elapsed: {elapsed}")
            self._last_checkpoint = now

    def summary(self):
        """Summarizes the counts of sequences by size."""
        h1 = "="*40        
        h2 = "_"*40
        print("\n")
        print(h1)
        print(f"   Contiguous Sequence Counts by Size")
        print(h2)        
        d = {"k": self._sequence_counts.keys(),"#":self._sequence_counts.values()}
        df = pd.DataFrame(data=d)
        print(df.to_string(index=False))         


        
