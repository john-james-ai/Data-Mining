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
# Last Modified : Monday, February 22nd 2021, 11:19:33 am                     #
# Modified By   : John James (john.james@nov8.ai)                             #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2021 nov8.ai                                                  #
# =========================================================================== #
#%%
import collections
from collections import OrderedDict
import itertools
from operator import itemgetter
import numpy as np
import pandas as pd
import time

from IO import IO
from sequence import Sequences
# --------------------------------------------------------------------------- #
class GSP:
    def __init__(self, infilepath, outfilepath, minrelsup=0.01):
        self._infilepath = infilepath
        self._outfilepath = outfilepath
        self._db = OrderedDict()            # Sequence database
        self._minrelsup = minrelsup         # Relative minimum support
        self._minsup = 0                    # Absolute minimum support        
        self._sequence_id = 0               # Sequence sequence number
        self._L = Sequences()               # all frequent sequences
        self._Lk = Sequences()              # all k-sequences that are frequent         
        self._complete = False              # True when all frequent sequences mined.
        self._io = None                     # Object responsible for file IO     
        self._start_time = None
        self._end_time = None 

    def _start(self):
        """Loads, maps, and creates the transaction database as a Pandas DataFrame."""    
        print("="*50)
        print("  Frequent Contiguous Sequence Mining using GSP")
        print("-"*50)
        self._start_time = time.time()
        self._io = IO()
        self._db = self._io.read(self._infilepath)           
        self._minsup = self._minrelsup * len(self._db)     
        #self._minsup = 2 # Delete and undelete prior line before submission

    def _end(self):
        """Write L, all frequent sequences, to file."""
        # Convert integers back to strings
        Lk = self._L.get_sequence_db()
        # Write sequences to file
        self._io.write(Lk, self._outfilepath)       
        # Summarize and report elapsed time.
        self._end_time = time.time()
        e = round(self._end_time - self._start_time,3)
        # self._L.print()
        self._L.summary()
        print(f"Elapsed time: {e} seconds")         

    def _join(self, k):
        print(f"  Joining {k} frequent sequences")
        Ck = list(map(list,[itertools.permutations(sequence,k) for sequence in self._db]))        
        Ck = list(dict.fromkeys([sequence for sequences in Ck for sequence in sequences]))
        return Ck

    def _prune(self, Ck, k):
        print(f"  Pruning {k} frequent sequences")
        print(f"        Ck: \n{Ck}")
        Ck_pruned = []
        sequences = map(list, Ck)
        for sequence in sequences:
            hits = []
            for review in self._db:
                hits.append(any(map(lambda x: review[x:x + len(sequence)] == sequence, range(len(review) - len(sequence) + 1))))
            if sum(hits) >= self._minsup:
                Ck_pruned.append({"k": k, "id": self._sequence_id, "sequence": sequence, "support": sum(hits)})
        return Ck_pruned
   
    def _add_sequences(self, k, Ck):
        for sequence in Ck:            
            self._L.add_sequence(k, sequence)
            self._Lk.add_sequence(k, sequence)
            self._sequence_id += 1      

    def _gen_lk_sequences(self,k):
        Ck = self._join(k)
        Ck = self._prune(Ck, k)
        if len(Ck) == 0:
            self._complete = True
        else:
            self._add_sequences(k, Ck)        

    def _gen_L1_sequences(self):
        """Creates L1 frequent sequences as list of dictionaries."""
        # Get support for each item i.e. the number of rows in self._db in which the item exists.
        sequences = collections.Counter(itertools.chain(*map(set, self._db)))
        # Add to Sequences objects        
        for sequence, support in sequences.items():
            if support >= self._minsup: 
                d = {"k": 1, "id": self._sequence_id, "sequence": [sequence], "support": support}
                self._L.add_sequence(1, d)
                self._Lk.add_sequence(1,d)
                self._sequence_id += 1      

    def gen(self):
        self._start()
        self._gen_L1_sequences()
        self._L.print_status(1)
        k = 2
        while(not self._complete):
            self._gen_lk_sequences(k)            
            self._L.print_status(k)
            k += 1
        self._end()
        
        
if __name__ == '__main__':
    infilepath = "../data/input.txt"
    outfilepath = "../data/patterns.txt"

    gsp = GSP(infilepath=infilepath, outfilepath=outfilepath, minrelsup=0.01)
    gsp.gen()

#%%    
