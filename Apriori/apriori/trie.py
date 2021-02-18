# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Mining                                                       #
# File    : \trie.py                                                          #
# Python  : 3.9.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : nov8.ai                                                           #
# Email   : john.james@nov8.ai                                                #
# URL     : https://github.com/john-james-sf/Data-Mining/                     #
# --------------------------------------------------------------------------- #
# Created       : Wednesday, February 17th 2021, 9:30:24 pm                   #
# Last Modified : Wednesday, February 17th 2021, 9:30:24 pm                   #
# Modified By   : John James (john.james@nov8.ai)                             #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2021 nov8.ai                                                  #
# =========================================================================== #


class Node:

    def __init__(self, item=""):        
        "Nodes is a word."
        self.item = item # uniquely identifies the node
        self.itemset = [] or self.itemset.append(item) # 
        self._tids
        self.parents = {}
        self.children = {}
        self._is_itemset = False
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

    def mark_as_itemset(self):
        self._is_itemset = True

class Trie:
    def __init__(self):
        self.root = Node("root")
        self._current_node = self.root
        self._words_searched = []
        self._words_found = [] 

    def add_item(self, item):
        """Adds item to trie."""

        self._current_node = self.root
        # Add item to child list if not already there.
        if item not in self._current_node.children.keys():                
            self._current_node.add_child(Node(word))

        # Traverse to the child node
        self._current_node = self._current_node.children[word]

    def find_item(self, item):
        """ Search the trie and return support if found."""

        # set _current node to root
        self._current_node = self.root

        # If the _current node has the item as a child, 
        # add it to words found and traverse to that node
        if word in self._current_node.children.keys():
            self._words.found.append(word)
            self._current_node = self._current_node.children[word]

        # else if word is not among children, stop searching
        else:
            break
    
    # if words searched == words found, return the _current node, 
    # otherwise return false. (You can do that in Python :)
    if cmp(self._words_searched, self._words_found) == 0:
        return self._current_node
    else:
        return False

