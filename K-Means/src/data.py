# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : K-Means++ Algorithm                                               #
# File    : \data.py                                                          #
# Python  : 3.9.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Course  : Introduction to Data Mining (Spring '21)                          #
# Email   : jtjames2@illinois.edu                                             #
# URL     : https://github.com/john-james-sf/Data-Mining/                     #
# --------------------------------------------------------------------------- #
# Created       : Saturday, April 24th 2021, 3:23:39 am                       #
# Last Modified : Saturday, April 24th 2021, 10:24:33 am                      #
# Modified By   : John James (jtjames2@illinois.edu)                          #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2021 nov8.ai                                                  #
# =========================================================================== #
#%%
import os
from collections import OrderedDict
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


# --------------------------------------------------------------------------- #
class IO:
    def __init__(self, standardize=True):        
        """Performs reads and optionally standardizes the data."""
        self._standardize = standardize        

    def read(self, filepath):
        """Loads datas into a DataFrame."""   
        data = pd.read_csv(filepath)
        if self._standardize:
            scaler = StandardScaler()
            data = scaler.fit_transform(data)
        return data
            
    def write(self, output, filepath):
        pd.to_csv(filepath, sep=" ", header=None)
