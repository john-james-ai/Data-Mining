# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Frequent Sequence Pattern Mining                                  #
# File    : \trie.py                                                          #
# Python  : 3.9.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Course  : Introduction to Data Mining (Spring '21)                          #
# Email   : jtjames2@illinois.edu                                             #
# URL     : https://github.com/john-james-sf/Data-Mining/                     #
# --------------------------------------------------------------------------- #
# Created       : Monday, April 19th 2021, 10:00:18 am                        #
# Last Modified : Monday, April 19th 2021, 1:38:14 pm                         #
# Modified By   : John James (jtjames2@illinois.edu)                          #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2021 nov8.ai                                                  #
# =========================================================================== #
#%%
from typing import Dict

class Node:
    """Represents a string, a concatenation of labels at d0:dn-1."""

    def __init__(self, label = ''):
        """Initializes Node with empty string and no children."""        
        self.label = label          # None if root node.
        self.parent = None          # None if root node.
        self.children = dict()        
        self.support = 0
        self.is_word = False
        self.is_leaf = False

    def __str__(self):
        return f'{self.label} ({self.support}) -> {self.children}'

class Trie:
    """A top-down tree structure representation of the transaction database."""
    def __init__(self):
        self.root = Node()

    def display(self):
        """Prints the contents of this prefix tree."""
        print('======================================================')
        self.__displayHelper(self.root)
        print('======================================================\n')


    def __displayHelper(self, current):
        """ Private helper for printing the contents of this prefix tree."""
        print(current)
        for letter in current.children:
            self.__displayHelper(current.children[letter])


    def insert(self, word):
        """Inserts the given word into this trie."""
        current = self.root
        for i, char in enumerate(word):
            if char not in current.children:
                prefix = word[0:i+1]
                current.children[char] = Node(prefix)
            current = current.children[char]
        current.is_word = True
        current.support += 1


    def find(self, word):
        """Returns the Node (word) if it exists and None otherwise."""
        current = self.root
        for char in word:
            if char in current.children:                
                current = current.children[char]
            else:
                return None

        if current.is_word: return current


    def _child_words_for(self, node, words):
        """ Recursively adds words from children nodes.

        Cycles through all children of node recursively, adding 
        them to words if they constitute whole words 
        """
        if node.is_word:
            words.append(node.label)
        for letter in node.children:
            self._child_words_for(node.children[letter], words)


    def starts_with(self, prefix):
        """ Returns words that start with the prefix.
        
        Returns a list of all words beginning with the given prefix, or
        an empty list if no words begin with that prefix.
        """
        words = list()
        current = self.root
        for char in prefix:
            if char not in current.children:
                # Could also just do return words since it's empty
                return list()
            current = current.children[char]
        
        self._child_words_for(current, words)
        return words


    def size(self, current = None):
        """ Returns total number of nodes in trie."""
        # By default, get the size of the whole trie, but
        # allow the user to get the size of any subtrees as well
        if not current:
            current = self.root
        count = 1
        for letter in current.children:
            count += self.size(current.children[letter])
        return count

if __name__ == '__main__':
    trie = Trie()
    trie.insert('apple')
    trie.insert('app')
    trie.insert('aposematic')
    trie.insert('appreciate')
    trie.insert('book')
    trie.insert('bad')
    trie.insert('bear')
    trie.insert('bat')
    trie.insert('bat')
    print(trie.display())
#%%%