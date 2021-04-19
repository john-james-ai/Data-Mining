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
item = [(1,2,3)]
item = map(list,item)
s1 = set(item)
data = [[1,2,3],[1,2,3,6,8,9],[1,2,3,1,2,3], [4,5,6]]
s2 = set(data)
ck = [i for i in item if i in data]
print(ck)
#%%