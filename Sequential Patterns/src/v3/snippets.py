# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Frequent Sequence Pattern Mining                                  #
# File    : \snippets.py                                                      #
# Python  : 3.9.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Course  : Introduction to Data Mining (Spring '21)                          #
# Email   : jtjames2@illinois.edu                                             #
# URL     : https://github.com/john-james-sf/Data-Mining/                     #
# --------------------------------------------------------------------------- #
# Created       : Thursday, April 22nd 2021, 11:04:35 am                      #
# Last Modified : Thursday, April 22nd 2021, 2:34:36 pm                       #
# Modified By   : John James (jtjames2@illinois.edu)                          #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2021 nov8.ai                                                  #
# =========================================================================== #
# Find the indices of a sequence in a list.
#%%
# Gets the indexes (start and end) of b in a
a = [2,3,5,2,5,6,7,2,5,6]
b = [2,5,6]
c = [3,1]
print([(i, i+len(b)) for i in range(len(a)) if a[i:i+len(b)] == b][0])
# Find just first index
print([i for i in range(len(a)) if a[i:i+len(b)] == b])
# indices including suffix of 1
d = [(i,i+len(c)+1) for i in range(len(a)) if a[i:i+len(c)] == c]
print(d)



# Checks if list a is in list b
def list_in(a, b):
    return any(map(lambda x: b[x:x + len(a)] == a, range(len(b) - len(a) + 1)))
a = [0, 0, 7]
b = [1, 0, 0, 7, 3]
c = [7, 0, 0, 0]
print(list_in(a, b))
print(list_in(a, c))

d = [b,c]
sum([list_in(a,x) for x in d])
