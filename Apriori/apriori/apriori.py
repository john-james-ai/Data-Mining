# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Mining                                                       #
# File    : \apriori.py                                                       #
# Python  : 3.9.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : nov8.ai                                                           #
# Email   : john.james@nov8.ai                                                #
# URL     : https://github.com/john-james-sf/Data-Mining/                     #
# --------------------------------------------------------------------------- #
# Created       : Thursday, February 11th 2021, 8:44:58 am                    #
# Last Modified : Wednesday, February 17th 2021, 11:29:15 am                  #
# Modified By   : John James (john.james@nov8.ai)                             #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2021 nov8.ai                                                  #
# =========================================================================== #
class Node:

    def __init__(self, word=""):        
        "Nodes is a word."
        self.word = word # uniquely identifies the node
        self.phrase = [] or self.phrase.append(word) # 
        self._tids
        self.parents = {}
        self.children = {}
        self._is_item = False
        self._support = 1
    
    def add_parent(self, parent):
        """Adds a parent to the node, indexed by the text of the parent node."""
        self._parents[parent.word] = parent
        self.phrase.append(parent.phrase)

    def add_child(self, child):
        """Adds a child node, indexed by text of child node, and bumps support."""
        self._children[child.word] = child
        self._support += 1

    def get_support(self):        
        return self._support

    def mark_as_item(self):
        self._is_itemset = True

class Trie:
    def __init__(self):
        self.root = Node("root")
        self.current_node = self.root
        self._words_searched = []
        self._words_found = [] 

    def add_item(self, item):
        """Splits item, either word or phrase, to trie."""
        words = item.split()
        for word in words:
            # Add word to child list if not already there.
            if word not in self.current_node.children.keys():                
                self.current_node.add_child(Node(word))

            # Traverse to the child node
            self.current_node = self.current_node.children[word]

        # Mark the last node as an item
        self.current_node.is_itemset = True

    def find_item(self, item):
        """ Search the trie and return support if found."""

        # set current node to root
        self.current_node = self.root

        # initialize words searched and found
        self._words_searched = item.split()
        self._words_found = []

        # traverse until found or end of branch.
        for word in self._words_searched:

            # If the current node has the word as a child, 
            # add it to words found and traverse to that node
            if word in self.current_node.children.keys():
                self._words.found.append(word)
                self.current_node = self.current_node.children[word]

            # else if word is not among children, stop searching
            else:
                break
        
        # if words searched == words found, return the current node, 
        # otherwise return false. (You can do that in Python :)
        if cmp(self._words_searched, self._words_found) == 0:
            return self.current_node
        else:
            return False

















    

