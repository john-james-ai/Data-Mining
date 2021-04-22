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
# Last Modified : Monday, April 19th 2021, 12:45:54 pm                        #
# Modified By   : John James (jtjames2@illinois.edu)                          #
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
from datetime import datetime

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
        now = datetime.now() 
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        self._start_time = time.time()
        self._io = IO()
        self._db = np.array(self._io.read(self._infilepath), dtype=object)
        print(type(self._db))
        print(self._db[0:5])           

        self._minsup = self._minrelsup * len(self._db)          
        #self._minsup = 2 # Delete and undelete prior line before submission

        print("="*50)
        print("  Frequent Contiguous Sequence Mining using GSP")
        print(f"            {date_time}")
        print(f"      Minimum Support: {self._minsup} ")
        print(f"        Database Size: {len(self._db)}")
        print("-"*50)        

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

    def _search_sequence(self, seq,review):
        """Find a sequence in an array

        Parameters 
        ----------
        seq : input 1D array of integers
        review : input 1D array of integers

        Output
        ------
        indices : 1D array of indices of the occurence of seq
        in review. If seq is not found in review, an empty
        list is returned.

        Reference: https://stackoverflow.com/questions/36522220/searching-a-sequence-in-a-numpy-array
        """
        # Convert lists to numpy arrays
        seq = np.array(seq)
        # Store the sizes of the sequence and review
        seq_size, review_size = seq.size, review.size

        # Range of sequence
        seq_range = np.arange(seq_size)

        # Create a 2D array of sliding indices across the entire length
        # of the review. Match with the input sequence and return the 
        # matching starting indices.
        M = (review[np.arange(review_size-seq_size+1)[:,None]+ seq_range] == seq).all(1)    

        # Get the range of those indices as final output
        if M.any() > 0:
            indices = np.where(np.convolve(M, np.ones((seq_size), dtype=int))>0)[0]
        else:
            indices = np.array([])
        # Return 1 if found, i.e. len(indices) > 0, otherwise return 0
        if indices.size > 0:
            return 1
        else:
            return 0



    def _join(self, k):
        print(f"       Joining {k} frequent sequences")
        Ck = list(map(list,[itertools.permutations(sequence,k) for sequence in self._db]))        
        Ck = list(dict.fromkeys([sequence for sequences in Ck for sequence in sequences]))
        return Ck

    def _prune(self, Ck, k):
        print(f"       Pruning {k} frequent sequences")     
        previous = time.time()
        Ck_pruned = []
        sequences = map(list, Ck)
        for sequence in sequences:
            hits = 0
            for review in self._db:
                hits += self._search_sequence(sequence, review)
            if hits >= self._minsup:
                now = time.time()
                elapsed = round(now-previous,3)
                print(f"          Adding the following {k}-sequence: {sequence} with support: {{{hits}}}. {elapsed} seconds elapsed.")
                previous = now
                Ck_pruned.append({"k": k, "id": self._sequence_id, "sequence": sequence, "support": hits})
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
    infilepath = "../data/reviews_sample.txt"
    outfilepath = "../data/patterns.txt"

    gsp = GSP(infilepath=infilepath, outfilepath=outfilepath, minrelsup=0.01)
    gsp.gen()

#%%    
