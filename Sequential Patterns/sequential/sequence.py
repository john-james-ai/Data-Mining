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
from collections import OrderedDict
from itertools import combinations
import numpy as np
import pandas as pd
# --------------------------------------------------------------------------- #
class Sequences:
    def __init__(self):
        self._sequences = OrderedDict()
        self._sequence_counts = OrderedDict()
        self.total_sequences = 0        

    def get_sequences(self, k):
        """Returns a list of sequences of size k."""        
        sequences = []
        sequence_list = self._sequences[k]
        for sequence in sequence_list:
            sequences.append(sequence["sequence"])
        return sequences

    def get_sequence_db(self, k=None):
        """This returns the entire sequence object or the k sequences"""
        if k:
            return self._sequences[k]
        else:
            return self._sequences

    def add_sequence(self, sequence):
        """Adds sequence to collection and updates counts."""
        #Get k. If k exists, append to list of sequences. Otherwise, create list

        if sequence["k"] in self._sequences.keys():
            # Append sequence to list            
            self._sequences[sequence["k"]].append(sequence)            
            self._sequence_counts[sequence["k"]] += 1
            self.total_sequences += 1
        else:
            sequences = []
            sequences.append(sequence)            
            self._sequences[sequence["k"]] = sequences
            self._sequence_counts[sequence["k"]] = 1
            self.total_sequences = 1

    def add_sequence_list(self, sequences):
        """Add a list of sequences. Used for L1 sequences."""
        for sequence in sequences:
            self.add_sequence(sequence)

    def replace_sequence(self, old, new):
        """Replaces old sequence with new sequence."""
        k = len(old)
        sequences = self.get_sequences(k)
        for idx, item in enumerate(sequences):
            if item == old:
                self._sequences[idx]["sequence"] = new
                break

    def join(self, k):
        

    def prune_candidates(self, k, Ck):
        """Prunes the candidates Ck, returning only those whose k-1 sequences are frequent."""         
        itemlist = []   # Candidates to return
        current_sequences = [i["sequence"] for i in self._sequences[k-1]]        
        current_sequences.sort()
        
        for candidate in Ck:                
            candidate_subsets = list(combinations(candidate, k-1))
            items_to_find = len(list(candidate_subsets))
            items_found = 0             # Initiate counters 
            current_sequences_ptr = 0    # Initiate pointer into current sequences
            subset_ptr = 0              # Initiate pointer into subset sequences
            
            assert (isinstance(candidate_subsets,list))
            while subset_ptr < len(candidate_subsets):
                cs = list(candidate_subsets[subset_ptr])                
                if len(cs) == 1:
                    cs = cs[0]
                while ((current_sequences_ptr < len(list(current_sequences))) and (items_found < items_to_find)):                
                    assert isinstance(current_sequences[current_sequences_ptr], (list,int))
                    if cs == current_sequences[current_sequences_ptr]:                        
                        items_found += 1
                        current_sequences_ptr += 1
                        if items_to_find == items_found:
                            break
                    elif cs > current_sequences[current_sequences_ptr]:
                        current_sequences_ptr += 1
                    else:
                        break
                if items_to_find == items_found:
                    itemlist.append(candidate)
                subset_ptr += 1   

        # Remove duplicates
        Lk = [] 
        [Lk.append(x) for x in itemlist if x not in Lk]          
        return Lk




    def _print_sequences(self, k):
        """Prints the k-ary sequences in tabular format."""
        d = self._sequences[k]
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


    def summary(self):
        """Summarizes the counts of sequences by size."""
        h1 = "="*40        
        h2 = "_"*40
        print("\n")
        print(h1)
        print(f"        Itemset Counts by Size")
        print(h2)        
        d = {"k": [k for k in self._sequence_counts.keys()], 
             "Num": [v for v in self._sequence_counts.values()]}
        df = pd.DataFrame(d)
        print(df)

        
if __name__ == '__main__':
    sequences = Sequences()
    for i in range(5):
        n_sequences = np.random.randint(1,10,1)            
        for j in range(n_sequences[0]):
            iset = {}
            iset["k"] = i+1
            if (i == 0):
                iset["sequence"] = int(np.random.randint(i,10,i+1))    
            else:
                iset["sequence"] = list(np.random.randint(1,10, i+1))
            iset["support"] = np.random.randint(1,100,1)
            sequences.add_sequence(iset)
    isets = sequences.get_sequences(1)
    print(isets)
    a = {"k": 3, "sequence": [1,2,3], "support": 30}
    b = {"k": 3, "sequence": [1,2,5], "support": 30}
    c = {"k": 3, "sequence": [1,3,5], "support": 30}
    d = {"k": 3, "sequence": [2,3,5], "support": 30}
    e = {"k": 3, "sequence": [2,3,7], "support": 30}
    f = {"k": 3, "sequence": [2,5,7], "support": 30}
    g = {"k": 3, "sequence": [3,5,7], "support": 30}
    candidates = [a,b,c,d,e,f,g]
    sequences.add_sequence_list(candidates)    
    sequences.print()
    sequences.summary()    
    p = [ (1,2,3,5),(2,3,5,7), (6,3,5,2), (9,7,1,5)]
    print(sequences.prune_candidates(4,p))    
    p = [ (1,2),(2,3), (3,6), (7,9)]
    print(sequences.prune_candidates(2,p))    
#%%
            


