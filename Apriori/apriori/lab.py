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
# Created       : Friday, February 19th 2021, 12:57:56 pm                     #
# Last Modified : Friday, February 19th 2021, 12:57:57 pm                     #
# Modified By   : John James (john.james@nov8.ai)                             #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2021 nov8.ai                                                  #
# =========================================================================== #
#%%
from collections import OrderedDict
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
# --------------------------------------------------------------------------- #
d1 = {"k":3, "itemset": [3,4,8], "support": 14}
d2 = {"k":3, "itemset": [3,4,18], "support": 5}
collection = OrderedDict()
collection[1] = {"soomething": "else"}
print(collection)
itemsets = []
itemsets.append(d1)
itemsets.append(d2)
collection[d1["k"]] = itemsets

print(collection)
