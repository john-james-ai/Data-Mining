# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Frequent Sequence Pattern Mining                                  #
# File    : \lab.py                                                           #
# Python  : 3.9.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Course  : Introduction to Data Mining (Spring '21)                          #
# Email   : jtjames2@illinois.edu                                             #
# URL     : https://github.com/john-james-sf/Data-Mining/                     #
# --------------------------------------------------------------------------- #
# Created       : Thursday, April 22nd 2021, 9:57:32 am                       #
# Last Modified : Thursday, April 22nd 2021, 10:02:57 am                      #
# Modified By   : John James (jtjames2@illinois.edu)                          #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2021 nov8.ai                                                  #
# =========================================================================== #
#%%
from itertools import chain
from collections import Counter
  
def countList(lst, x):
      
    return Counter(chain.from_iterable(set(i) for i in lst))[x]
      
# Driver Code
lst = [['a'], ['a', 'c', 'b'], ['d']] 
x = ['a','c']
print(x in lst)
print(any(sublist in x for sublist in lst))
#%%