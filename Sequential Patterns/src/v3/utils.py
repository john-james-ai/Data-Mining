# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Frequent Sequence Pattern Mining                                  #
# File    : \utils.py                                                         #
# Python  : 3.9.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Course  : Introduction to Data Mining (Spring '21)                          #
# Email   : jtjames2@illinois.edu                                             #
# URL     : https://github.com/john-james-sf/Data-Mining/                     #
# --------------------------------------------------------------------------- #
# Created       : Tuesday, April 20th 2021, 10:26:14 pm                       #
# Last Modified : Friday, April 23rd 2021, 4:00:45 pm                         #
# Modified By   : John James (jtjames2@illinois.edu)                          #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2021 nov8.ai                                                  #
# =========================================================================== #
import inspect
verbose = True
def announce():
  if verbose:
    print(f"Entering {inspect.stack()[1][3]}")

def leaving():
  if verbose:
    print(f"Leaving {inspect.stack()[1][3]}")    
