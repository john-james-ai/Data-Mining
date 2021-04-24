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
# Last Modified : Saturday, April 24th 2021, 2:07:13 am                       #
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
from utils import announce, leaving
# --------------------------------------------------------------------------- #
class SequentialPatterns:
    """The collection (list) of frequent SequentialPattern objects."""
    def __init__(self):
        self.sequential_patterns = OrderedDict()            
        self.count = 0

    def add_pattern(self, l, pattern):
        """Adds a single l-sequence pattern to the collection"""
        announce()
        self.count += 1
        if l in self.sequential_patterns.keys():
            self.sequential_patterns[l].append(pattern)
        else:
            self.sequential_patterns[l] = [pattern]
        leaving()
        
    def register_patterns(self, l, patterns):
        """Adds a list of l-sequence patterns to the collection at once."""
        sequences = []
        for pattern in patterns:
            self.add_pattern(l, pattern)
            sequences.append(pattern["sequence"])
        return sequences        
        
    def _print_header(self,l):
        h1 = "="*40        
        h2 = "_"*40
        print("\n")
        print(h1)
        print(f"  Sequential Patterns Prefix Size: {l}")
        print(h2)    

    def _print_footer(self):
        h2 = "_"*40
        print(h2)    

    def print(self, l=None):
        """Prints all sequences."""
        if l is not None:
            self._print_header(l)
            for pattern in self.sequential_patterns[l]:                
                print(f"{pattern['sequence']}: support: {pattern['support']}")
            self._print_footer()
        else:
            for size, patterns in self.sequential_patterns.items():
                self._print_header(size)
                for pattern in patterns:
                    print(f"{pattern['sequence']}: support: {pattern['support']}")
                self._print_footer()
# --------------------------------------------------------------------------- #
class Candidate:
    """A sequence and its support. """
    def __init__(self, sequence):
        self.sequence = sequence
        self.support = 1
        self.id = self.hash()

    def hash(self):
        return sum(self.sequence)

        
# --------------------------------------------------------------------------- #
class Candidates:
    """Accumulates support for candidates and returns frequent sequences."""
    def __init__(self, minsup=2):
        self.minsup = minsup
        self.candidates = {}

    def _exists(self, candidate):
        found = False
        if candidate.id in self.candidates.keys():
            found = True            
        return found

    def add(self, candidate):
        if self._exists(candidate):
            self.candidates[candidate.id].support += 1
        else:
            self.candidates[candidate.id] = candidate

    def get_frequent(self):
        candidates = []
        for idx, candidate in self.candidates.items():            
            if candidate.support  >= self.minsup:
                d = {"sequence": candidate.sequence, "support": candidate.support}
                candidates.append(d)
        return candidates

# --------------------------------------------------------------------------- #
class ProjectedDB:                    
    """Projected database for a given prefix and a prior projected database."""
    def __init__(self, prefix, projected_db):
        self.prefix = prefix
        self._projected_db = projected_db
        self.projection = []

    def create_projections(self):
        """Generates the projections from the designated prefix."""        
        announce()
        for row in self._projected_db:
            # Find indices of sequences matching the prefix in the projected database.
            indices = [i for i in range(len(row)) if row[i:i+len(self.prefix)] == self.prefix]
            # Check to confirm a sequence was found.
            if len(indices) > 0:
                # Get index that marks the start of the first occurrence of the prefix
                index = indices[0]
                # The projection (including the prefix) goes to the end of the row.
                projection = row[index:]
                self.projection.append(projection)
        leaving()
        return self.projection
  
    def print(self):
        print(f"{self.prefix}: {self.suffixes}")

# --------------------------------------------------------------------------- #
class PrefixSpan:
    def __init__(self, sequential_db, minrelsup=0.01):
        self._sequential_db = sequential_db     # Sequence database
        self._minrelsup = minrelsup             # Relative minimum support
        self._minsup = 0                        # Absolute minimum support
        self._sequential_patterns = SequentialPatterns()  # all frequent sequences        
        self._complete = False                  # True when all frequent sequences mined.
        self._start_time = None
        self._end_time = None 

    def _start(self):
        """Sets minimum support and starts the clock.""" 
        now = datetime.now() 
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        self._start_time = time.time()        

        self._minsup = max(2,self._minrelsup * len(self._sequential_db))          

        print("="*50)
        print("  Frequent Contiguous Sequence Mining using PrefixSpan")
        print(f"            {date_time}")
        print(f"      Minimum Support: {self._minsup} ")
        print(f"        Database Size: {len(self._sequential_db)}")
        print("-"*50)        

    def _end(self):
        """Stops the clock."""
        self._end_time = time.time()
        # Obtains sequential patterns as a list of dictionaries.
        self._status()  

    def _gen_l1_sequential_patterns(self, prefix, l, projected_db):
        """Creates l1 frequent sequences as list of dictionaries."""
        announce()        
        # Extract l1 candidates with support
        candidates = collections.Counter(itertools.chain(*map(set, projected_db)))        
        # Obtain l1 sequences with minimum support        
        sequential_patterns = [{"sequence":[item], "support": support} for item, support in candidates.items() if support >= self._minsup]
        # Register the sequential pattern with support and the method returns the sequences
        sequences = self._sequential_patterns.register_patterns(l, sequential_patterns)        
        return sequences

    def _gen_ln_sequential_patterns(self, prefix, l, projected_db):
        """Generates l>1 sequential patterns."""
        announce()
        candidates = Candidates(self._minsup)
        
        # Obtain sequences of length l that follow the prefix
        for row in projected_db:            
            # Find the indices   of the suffix that follows the prefix
            indices = [i for i in range(len(row)) if row[i:i+len(prefix)] == prefix]
            # Check to see an item was found
            if len(indices) > 0:                
                # Get index that mark the start and end of the first sequence that includes the prefix
                start = indices[0]
                end = start + len(prefix) + 1
                # Confirm that the prefix isn't at the end of the row.
                if end <= len(row):
                    # Obtain the sequence
                    sequence = row[start:end]
                    candidate = Candidate(sequence)
                    candidates.add(candidate)
        
        sequential_patterns = candidates.get_frequent()        
        sequences = self._sequential_patterns.register_patterns(l, sequential_patterns)       
        
        leaving()
        return sequences

    def _scan_projected_db(self, prefix, l, projected_db):
        """Scans projected databases for frequent sequences"""
        announce()
        if l == 0:
            sequences = self._gen_l1_sequential_patterns(prefix, l, projected_db)
        else:
            sequences = self._gen_ln_sequential_patterns(prefix, l, projected_db)
        
        leaving()
        return sequences

    def prefix_span(self, prefix, l, projected_db):        
        announce()         

        sequences = self._scan_projected_db(prefix, l, projected_db)
        if len(sequences) > 0:
            
            # For each sequential pattern, append to prefix and construct a projected database.
            for item in sequences:
                projected_db = ProjectedDB(prefix=item, projected_db=projected_db).create_projections()
                self.prefix_span(item, l+1, projected_db)
        leaving()


    def mine(self):
        self._start()
        sequences = self._gen_l1_sequential_patterns([], l=0, projected_db=self._sequential_db)
        for sequence in sequences:
            projected_db = ProjectedDB(prefix=sequence, projected_db=self._sequential_db).create_projections()
            self.prefix_span(sequence, l=1,projected_db=projected_db)
            self._status()

        self._end()        
        return self._sequential_patterns.sequential_patterns

    def _status(self):
        current_time = time.time()
        e = round(current_time - self._start_time,3)        
        n = self._sequential_patterns.count        
        print(f"{n} Frequent Contiguous Sequential Patterns Mined. Elapsed time: {e} seconds")                            
        
def main(infilepath, outfilepath):
    # Obtain the sequences as a list of lists
    io = IO()
    sequential_db = io.read(infilepath)
        
    # Create the prefix span object and mine frequent contiguous sequential patterns.
    ps = PrefixSpan(sequential_db, minrelsup=0.01)
    sequential_patterns = ps.mine()    

    # Write sequential patterns to output
    io.write(sequential_patterns, outfilepath)

        
if __name__ == '__main__':
    infilepath = "../../data/reviews_sample.txt"
    outfilepath = "../../data/patterns.txt"
    main(infilepath, outfilepath)

#%%    
