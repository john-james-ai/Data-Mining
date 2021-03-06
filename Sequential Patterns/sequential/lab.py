# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Mining                                                       #
# File    : \lab.py                                                           #
# Python  : 3.9.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : nov8.ai                                                           #
# Email   : john.james@nov8.ai                                                #
# URL     : https://github.com/john-james-sf/Data-Mining/                     #
# --------------------------------------------------------------------------- #
# Created       : Thursday, March 4th 2021, 8:21:10 pm                        #
# Last Modified : Thursday, March 4th 2021, 8:21:11 pm                        #
# Modified By   : John James (john.james@nov8.ai)                             #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2021 nov8.ai                                                  #
# =========================================================================== #
#%%
import itertools, collections
import numpy as np
# Generate generate sequences of length n
x = [0,1,7,3,4,5,10,1,7,3,4]
n = 2
y = list(map(list,zip(*(x[i:] for i in range(n)))))
# Count occurrence of subsequence in sequence. 
print(y)
print(len([i for i in y if i == [1,7]]))
# n = 3
n = 3
y = list(map(list,zip(*(x[i:] for i in range(n)))))
print("\n")
print(y)
print(len([i for i in y if i == [1,7,3]]))
# n = 4
n = 4
y = list(map(list,zip(*(x[i:] for i in range(n)))))
print("\n")
print(y)
print(len([i for i in y if i == [1,7,3,4]]))
counter = collections.Counter(y)
print("\n")
print(counter)
# Flatten list and count elements
data = [[1,2,3],[1,1,1]]
counter = collections.Counter(itertools.chain(*data))
print("\n")
print(counter)
# Count occurrences of sequences
def count_sequence(lst, seq):
     count = 0
     len_seq = len(seq)
     upper_bound = len(lst)-len_seq+1
     for i in range(upper_bound):
         if lst[i:i+len_seq] == seq:
             count += 1
     return count
# %%
