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
import numpy as np
x = [0,1,7,3,4,5,10,1,7,3]
n = 3
y = map(list,zip(*(x[i:] for i in range(n))))
print(len([i for i in y if i == [1,7,3]]))
print([i for i in y])


# %%
