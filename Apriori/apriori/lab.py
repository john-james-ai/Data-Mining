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
from itertools import combinations
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
# --------------------------------------------------------------------------- #
a = [1,2,3,5,6]
b = combinations(a, 3)
for c in b:
    print(c)

d = set(b)
print(d)
