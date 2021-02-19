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
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
# --------------------------------------------------------------------------- #
a = ["home and car, bar & restaurant; hit; bump; toke;"]
b = ["one and two, three; a,b,c; red,green,blue,yellow; a,b,c; toke;"]
a = a[0].split(";")
b = b[0].split(";")
c = np.concatenate((a,b), axis=0)
print(c)
c = c[0].split(";").split(",")
print(c)
e = LabelEncoder()
c_e = e.fit_transform(c)
print(c_e)
c_d = e.inverse_transform(c_e)
print(c_d)
assert((c == c_d).all())
i = [3,2,2,5,7,1]
i_d = e.inverse_transform(i)
print(i_d)
