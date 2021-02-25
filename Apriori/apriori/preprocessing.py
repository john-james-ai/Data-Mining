# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Mining                                                       #
# File    : \data.py                                                          #
# Python  : 3.9.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : nov8.ai                                                           #
# Email   : john.james@nov8.ai                                                #
# URL     : https://github.com/john-james-sf/Data-Mining/                     #
# --------------------------------------------------------------------------- #
# Created       : Friday, February 19th 2021, 4:45:30 pm                      #
# Last Modified : Friday, February 19th 2021, 4:45:51 pm                      #
# Modified By   : John James (john.james@nov8.ai)                             #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2021 nov8.ai                                                  #
# =========================================================================== #
#  This module performers data encoding operations required by the Apriori    #
#  implementation.                                                            #
# =========================================================================== #
#%%
from collections import OrderedDict
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from IO import IO
# --------------------------------------------------------------------------- #
class AprioriDatafy:
    def __init__(self):
        self._database = None
        self._encoder = None

    def fit(self, X=None):
        """Creates the encoding map."""
        self._encoder = Encoder()
        self._database = self._encoder.fit_transform(X)
        self._database = pd.Series(self._database)        
    
    def transform(self, X=None):
        """Converts encoded data to one-hot dataframe format."""
        mlb = MultiLabelBinarizer()
        self._database = pd.DataFrame(mlb.fit_transform(self._database),
                                        columns=mlb.classes_,
                                        index=self._database.index)
        return self._database

    def fit_transform(self, X=None):
        """Convenience and nod to scikit-learn."""
        self.fit(X)
        return self.transform(X)    

    def inverse_transform(self, X=None):
        return self._encoder.inverse_transform(X)


class Encoder:
    def __init__(self):
        self._forward_mapping = OrderedDict()
        self._inverse_mapping = OrderedDict()        
        self._items = set()

    def fit(self, X):
        """Creates a set of unique values in X, and a mapping dictionaries."""
        self._items = set()
        self._forward_mapping = OrderedDict()
        self._inverse_mapping = OrderedDict()
        [[self._items.add(item) for item in itemslist] for _, itemslist in X.items()]
        self._items = sorted(self._items)
        for idx, item in enumerate(self._items):            
            self._forward_mapping[item] = idx
            self._inverse_mapping[idx] = item
    
    def transform(self, X):
        """Encodes the values of the X."""
        a = []
        for idx, items in X.items():
            encoded_items = []
            for item in sorted(items):
                encoded_items.append(self._forward_mapping.get(item))
            a.append(encoded_items)
        return a

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)        

    def _inverse_transform_L1(self, X):
        """ Inverse transforms L1 itemsets back to string representation."""
        result = []
        itemset_db = X.get_itemset_db(k=1)

        for itemset_object in itemset_db:
            output = OrderedDict()
            output["support"] = itemset_object["support"]
            output["itemset"] = self._inverse_mapping.get(itemset_object["itemset"])           
            result.append(output)
        return result        

    def _inverse_transform_Lk(self, X):
        """ Inverse transforms Lk (k>=2) back to string representation."""        
        result = []
        itemset = []      
        itemset_db = X.get_itemset_db()        

        for k, itemset_object_list in itemset_db.items():
            if k > 1:
                for itemset_object in itemset_object_list:
                    itemset = []
                    output = OrderedDict()
                    output["support"] = itemset_object["support"]                    
                    for j in range(len(itemset_object["itemset"])):
                        itemset.append(self._inverse_mapping.get(itemset_object["itemset"][j]))           
                    output["itemset"] = itemset
                    result.append(output)
        return result

    def inverse_transform(self, X):
        """Decodes numberic data back to original strings."""        
        
        L1 = self._inverse_transform_L1(X)
        Lk = self._inverse_transform_Lk(X)
        Lk = L1 + Lk
        return L1, Lk

                
# --------------------------------------------------------------------------- #
class DictEncoder:
    def __init__(self):
        self._forward_mapping = OrderedDict()
        self._inverse_mapping = OrderedDict()        
        self._items = set()

    def fit(self, X):
        """Creates a set of unique values in X, and a mapping dictionaries."""
        self._items = set()
        self._forward_mapping = OrderedDict()
        self._inverse_mapping = OrderedDict()
        [[self._items.add(item) for item in itemslist] for _, itemslist in X.items()]
        # for line, itemslist in X.items():
        #     for item in itemslist:
        #         self._items.add(item)
        self._items = sorted(self._items)
        for idx, item in enumerate(self._items):
            self._forward_mapping[item] = idx
            self._inverse_mapping[idx] = item
    
    def transform(self, X):
        """Encodes the values of the X."""
        d = OrderedDict()
        for idx, items in X.items():
            encoded_items = []
            for item in sorted(items):
                encoded_items.append(self._forward_mapping.get(item))
            d[idx] = encoded_items
        return d

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)        

    def inverse_transform(self, X):
        """Decodes values from a dict back into original values."""
        d = OrderedDict()
        for idx, items in X.items():
            decoded_items = []
            for item in items:
                decoded_items.append(self._inverse_mapping.get(item))
            d[idx] = decoded_items
        return d
#%%
