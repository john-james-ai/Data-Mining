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
from collections import Counter
import numpy as np
# Flatten list and count elements
item = [(1,2), (6,8,9)]
item = map(list,item)
print(item)
data = [[1,2,3],[1,2,3,6,8,9],[1,2,3,1,2,3], [4,5,6]]
def list_in(a, b):
    for item in a:
        hits = []    
        for review in b:
            hits.append(any(map(lambda x: review[x:x + len(item)] == item, range(len(review) - len(item) + 1))))
        print(sum(hits))
print(list_in(item, data))
# %%
