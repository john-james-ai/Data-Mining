# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Mining                                                       #
# File    : \itemset.py                                                       #
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
class Itemsets:
    def __init__(self):
        self._itemsets = OrderedDict()
        self._itemset_counts = OrderedDict()
        self.total_itemsets = 0        

    def get_itemsets(self, k):
        """Returns a list of itemsets of size k."""        
        itemsets = []
        itemset_list = self._itemsets[k]
        for itemset in itemset_list:
            itemsets.append(itemset["itemset"])
        return itemsets

    def get_itemset_db(self, k=None):
        """This returns the entire itemset object including support,k, and id"""
        if k:
            return self._itemsets[k]
        else:
            return self._itemsets

    def add_itemset(self, itemset):
        """Adds itemset to collection and updates counts."""
        #Get k. If k exists, append to list of itemsets. Otherwise, create list

        if itemset["k"] in self._itemsets.keys():
            # Append itemset to list            
            self._itemsets[itemset["k"]].append(itemset)            
            self._itemset_counts[itemset["k"]] += 1
            self.total_itemsets += 1
        else:
            itemsets = []
            itemsets.append(itemset)            
            self._itemsets[itemset["k"]] = itemsets
            self._itemset_counts[itemset["k"]] = 1
            self.total_itemsets = 1

    def add_itemset_list(self, itemsets):
        """Add a list of itemsets. Used for L1 itemsets."""
        for itemset in itemsets:
            self.add_itemset(itemset)

    def replace_itemset(self, old, new):
        """Replaces old itemset with new itemset."""
        k = len(old)
        itemsets = self.get_itemsets(k)
        for idx, item in enumerate(itemsets):
            if item == old:
                self._itemsets[idx]["itemset"] = new
                break

        

    def prune_candidates(self, k, Ck):
        """Prunes the candidates Ck, returning only those whose k-1 itemsets are frequent."""         
        itemlist = []   # Candidates to return
        current_itemsets = [i["itemset"] for i in self._itemsets[k-1]]        
        current_itemsets.sort()
        print("\nCurrent Itemsets")
        print(current_itemsets)
        print(f"\nReceived the following candidates {Ck}")
        
        for candidate in Ck:                
            candidate_subsets = list(combinations(candidate, k-1))
            items_to_find = len(list(candidate_subsets))
            items_found = 0             # Initiate counters 
            current_itemsets_ptr = 0    # Initiate pointer into current itemsets
            subset_ptr = 0              # Initiate pointer into subset itemsets
            print(f"\nThere are {items_to_find} candidate subsets.")            
            print(f"There are {items_found} items found.")            
            
            assert (isinstance(candidate_subsets,list))
            while subset_ptr < len(candidate_subsets):
                cs = list(candidate_subsets[subset_ptr])                
                print(f"Searching for subset {cs}")
                if len(cs) == 1:
                    cs = cs[0]
                while ((current_itemsets_ptr < len(list(current_itemsets))) and (items_found < items_to_find)):                
                    print(f"Candidate subset: {cs}, Current: {current_itemsets[current_itemsets_ptr]}")                                    
                    print(f"Candidate subset: {type(cs)} type, Current: {type(current_itemsets[current_itemsets_ptr])} type.")   
                    assert isinstance(current_itemsets[current_itemsets_ptr], (list,int))
                    if cs == current_itemsets[current_itemsets_ptr]:                        
                        items_found += 1
                        current_itemsets_ptr += 1
                        print(f"Found  {items_found} items. Item = {cs}")                        
                        if items_to_find == items_found:
                            break
                    elif cs > current_itemsets[current_itemsets_ptr]:
                        current_itemsets_ptr += 1
                    else:
                        break
                if items_to_find == items_found:
                    print(f"Adding {candidate} to large list")
                    itemlist.append(candidate)
                subset_ptr += 1   

        # Remove duplicates
        Lk = [] 
        [Lk.append(x) for x in itemlist if x not in Lk]          
        return Lk




    def _print_itemsets(self, k):
        """Prints the k-ary itemsets in tabular format."""
        d = self._itemsets[k]
        df = pd.DataFrame(d)
        h1 = "="*40        
        h2 = "_"*40
        print("\n")
        print(h1)
        print(f"{k}-Itemsets")
        print(h2)
        print(df.to_string(index=False))           

    def print(self, k=None):
        if k:
            self._print_itemsets(k)
        else:
            for k_ in self._itemsets.keys():
                self._print_itemsets(k_)


    def summary(self):
        """Summarizes the counts of itemsets by size."""
        h1 = "="*40        
        h2 = "_"*40
        print("\n")
        print(h1)
        print(f"        Itemset Counts by Size")
        print(h2)        
        d = {"k": [k for k in self._itemset_counts.keys()], 
             "Num": [v for v in self._itemset_counts.values()]}
        df = pd.DataFrame(d)
        print(df)

        
if __name__ == '__main__':
    itemsets = Itemsets()
    for i in range(5):
        n_itemsets = np.random.randint(1,10,1)            
        for j in range(n_itemsets[0]):
            iset = {}
            iset["k"] = i+1
            if (i == 0):
                iset["itemset"] = int(np.random.randint(i,10,i+1))    
            else:
                iset["itemset"] = list(np.random.randint(1,10, i+1))
            iset["support"] = np.random.randint(1,100,1)
            itemsets.add_itemset(iset)
    isets = itemsets.get_itemsets(1)
    print(isets)
    a = {"k": 3, "itemset": [1,2,3], "support": 30}
    b = {"k": 3, "itemset": [1,2,5], "support": 30}
    c = {"k": 3, "itemset": [1,3,5], "support": 30}
    d = {"k": 3, "itemset": [2,3,5], "support": 30}
    e = {"k": 3, "itemset": [2,3,7], "support": 30}
    f = {"k": 3, "itemset": [2,5,7], "support": 30}
    g = {"k": 3, "itemset": [3,5,7], "support": 30}
    candidates = [a,b,c,d,e,f,g]
    itemsets.add_itemset_list(candidates)    
    itemsets.print()
    itemsets.summary()    
    p = [ (1,2,3,5),(2,3,5,7), (6,3,5,2), (9,7,1,5)]
    print(itemsets.prune_candidates(4,p))    
    p = [ (1,2),(2,3), (3,6), (7,9)]
    print(itemsets.prune_candidates(2,p))    
#%%
            


