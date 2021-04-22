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
# Last Modified : Thursday, April 22nd 2021, 7:35:04 am                       #
# Modified By   : John James (jtjames2@illinois.edu)                          #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2021 nov8.ai                                                  #
# =========================================================================== #
# This module is comprised of the following classes and functions:            #
#       
#%%
import collections
from collections import OrderedDict
import itertools
from operator import itemgetter
import numpy as np
import pandas as pd
import time
from datetime import datetime
from dataclasses import dataclass

from IO import IO
from sequence import SequentialPatterns
from utils import announce
# --------------------------------------------------------------------------- #
@dataclass
class Sequence:
    """A single line of input containing sequences"""
    sid: int
    sequence: list
    def print(self):
        print(f"SID: {self.sid} - {self.sequence}")

# --------------------------------------------------------------------------- #
class SequenceDB:
    """The collection of Sequence objects which comprise the input database."""
    def __init__(self):
        self._sequences = OrderedDict()

    def add(self,sequence):
        """Adds a sequence object to the sequence database."""
        self._sequences[sequence.sid] = sequence    

# --------------------------------------------------------------------------- #
@dataclass
class SequentialPattern:
    """A frequent sequential pattern along with its support."""    
    pid: int
    pattern: list
    support: int
    size: int
    def print(self):
        print(f"{self.support}: {self.pattern}")    
# --------------------------------------------------------------------------- #
class SequentialPatterns:
    """The collection (list) of frequent SequentialPattern objects."""
    def __init__(self):
        self.sequential_patterns = OrderedDict()                

    def add(self, l, pattern):
        """Adds a l-sequence pattern to the collection."""
        if not self.sequential_patterns.has_key(l):
            self.sequential_patterns = []
        self.sequential_patterns[l].append(pattern)

    def _print_header(self,l):
        h1 = "="*40        
        h2 = "_"*40
        print("\n")
        print(h1)
        print(f"{l}-SequentialPatterns")
        print(h2)    

    def _print_footer(self):
        h2 = "_"*40
        print(h2)    

    def print(self, l=None):
        """Prints all sequences of size l. If l is None, prints all sequences."""

        if l is not None:
            self._print_header(l)
            for sequence in self.sequences[l]:
                sequence.print()
            self._print_footer()
        else:
            for l, sequences in self.sequences.items():
                self._print_header(l)
                for sequence in sequences:
                    sequence.print()
                self._print_footer()
# --------------------------------------------------------------------------- #
@dataclass
class ProjectedDB:                    
    """Creates a projected database dictionary consisting of a prefix and a list of suffixes."""
    prefix: list
    suffixes: list
    def print(self):
        print(f"{self.prefix}: {self.suffixes}")


class PrefixSpan:
    def __init__(self, prefix, suffixes, minsup):
        self.prefix = prefix
        self.suffixes = suffixes
        self._minsup = minsup

    def _gen_sequences(self, l):
        """Find all l-sequences in the projected database (prefix+suffixes)"""
        sequences = []
        for review, sequence in enumerate(self.suffixes):
            for idx, item in enumerate(sequence):
                subsequence = self.prefix + self.suffixes[idx:idx+l]                
                if subsequence not in sequences:
                    sequences.append(subsequence)
        return sequences

    def _get_frequent_sequences(self, l, sequences):
        """Filters the list of sequences, returning only frequent."""
        frequent = []
        for candidate in sequences:
            support = 0
            for sequence in self.suffixes:
                if candidate in sequence:
                    support += 1        
            if support >= self._minsup:
                sequence = Sequence(candidate, support,l)
                frequent.append(sequence)
        return frequent

    def mine(self, l):
        """Returns all l-sequences that are frequent."""
        sequences = self._get_l_sequences(l)
        frequent = self._get_frequent_sequences(l, sequences)
        return frequent        

    def print(self):
        """Prints projected database."""
        print(f"Prefix: {prefix} | Projection: {suffixes}")
        

if __name__ == '__main__':
    infilepath = "../../data/input.txt"
    outfilepath = "../../data/output.txt"
    io = IO()
    db = Reviews(infilepath, minsup=2, io)
    db.load()
    l1_sequences = db.find_l1_sequences()
    sequences = SequentialPatterns(io)
    sequences.add(1, l1_sequences)
    sequences.print()
    sequences.save(outfilepath)





# --------------------------------------------------------------------------- #
class PrefixSpan:
    def __init__(self, infilepath, outfilepath, minrelsup=0.01):
        self._infilepath = infilepath
        self._outfilepath = outfilepath
        self._db = OrderedDict()            # Sequence database
        self._minrelsup = minrelsup         # Relative minimum support
        self._minsup = 0                    # Absolute minimum support
        self._sequences = SequentialPatterns()       # all frequent sequences        
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
        self._db = self._io.read(self._infilepath)        
        print(self._db)

        self._minsup = max(2,self._minrelsup * len(self._db))          

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

    def _get(self, alpha,l,pdb):        
        announce()  
        sequences = list()   

        # Find all l-sequences in pdb       
        for review, sequence in enumerate(pdb):
            for idx, item in enumerate(sequence):
                subsequence = pdb[review][idx:idx+(l+1)]
                if subsequence not in sequences:
                    sequences.append(subsequence)

        # Compute support for each sequence in pdb.
        for candidate in sequences:
            support = 0
            for sequence in pdb:
                if candidate in sequence:
                    support += 1
            

        
        print(f"Sequence before counting: {sequences}")
        sequences = collections.Counter([tuple(i) for i in sequences])        
        #sequences = collections.Counter(tuple(i) for i in sequences)        
        #sequences = collections.Counter(tuple(i) for i in pdb)        
        print(f"Sequence after counting: {sequences}")
        


    def _get_projected_database(self, alpha, db):
        announce()        
        pdb = []
        for review, sequence in enumerate(db):
            for idx, item in enumerate(sequence):
                if item == alpha:
                    pdb.append(db[review][idx:])
                    break
        #pdb = [db[row][idx:] for row, sequence in enumerate(db) for idx, item in enumerate(sequence) if item == alpha]
        print(f"\nProjecting {alpha}: {pdb}")
        return pdb

    def _gen_L1_sequences(self):
        announce()
        """Creates L1 frequent sequences as list of dictionaries."""
        # Get support for each item i.e. the number of rows in self._db in which the item exists.
        candidates = collections.Counter(itertools.chain(*map(set, self._db)))        
        # Extract frequent sequences of length 1
        frequent = {item:support for item, support in candidates.items() if support >= self._minsup}        
        # Create sequences object and add frequent sequences
        sequences = SequentialPatterns()
        sequences.add(1,frequent) 
        return sequences

    def mine(self):
        self._start()
        sequences = self._gen_L1_sequences()
        for sequence in sequences.keys():
            self._prefix_span(sequence,1,pdb)
        #self._prefix_span(self._)
        # self._L.print_status(1)
        # k = 2
        # while(not self._complete):
        #     self._gen_lk_sequences(k)            
        #     self._L.print_status(k)
        #     k += 1
        # self._end()
        
        
if __name__ == '__main__':
    infilepath = "../../data/input.txt"
    outfilepath = "../../data/output.txt"

    ps = PrefixSpan(infilepath=infilepath, outfilepath=outfilepath, minrelsup=0.01)
    ps.mine()

#%%    
