# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : K-Means++ Algorithm                                               #
# File    : \k-means.py                                                       #
# Python  : 3.9.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Course  : Introduction to Data Mining (Spring '21)                          #
# Email   : jtjames2@illinois.edu                                             #
# URL     : https://github.com/john-james-sf/Data-Mining/                     #
# --------------------------------------------------------------------------- #
# Created       : Saturday, April 24th 2021, 3:13:53 am                       #
# Last Modified : Saturday, April 24th 2021, 2:41:19 pm                       #
# Modified By   : John James (jtjames2@illinois.edu)                          #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2021 nov8.ai                                                  #
# =========================================================================== #
#%%
import os
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist 
from data import IO
class KMeans:
    """Runs the K-Means++ Algorithm (Arthur,Vassilvitskii 2007}"""
    def __init__(self, k=3, n_init=10, max_iter=300, rtol=1e-4, random_state=None):
        self.k = k
        self.n_init = n_init
        self.max_iter = max_iter
        self.rtol = rtol
        self.cluster_labels = range(k)
        self.random_state = random_state
        self.labels = None

    def initplusplus(self, X):
        """Does n_init trials of starts and selects centroids with lowest SSE"""
        n,p = X.shape
        trial_scores = []
        trial_centroids = np.zeros((self.n_init, n,self.k))
        for i in range(self.n_init):     
            print(f"Start # {i}")   
            n = X.shape[0]        
            centroids = np.zeros((self.k,p))
            # Choose initial point drawn from uniform random distribution.
            idx= np.random.randint(0,n)
            print(f"    Selected point {idx}")
            centroids[0] = X[idx,:]

            # Choose remaining points according to distribution proportional to D^2
            for j in range(1,self.k):                
                # Compute the squared distances between the centroid and each point and sort
                d2 = np.sort(np.square(np.sum(np.subtract(X,centroids[0,:]), axis=1)))
                print(f"    d2.shape {d2.shape}")
                # Compute the cumulative sum of squared distances
                cs = np.cumsum(d2, axis=0)
                # Make it a probability by dividing by the sum 
                print(f"    cs.shape {cs.shape}")
                # Select a point at random from this distribution.
                selection = np.random.uniform(0,n,1)
                # Find index of minimum cumsum value greater than the selected value
                idx = next(x for x, val in enumerate(cs) if val>selection)
                # Subtract 1 from the index to get the value just below selected value
                idx -= 1
                # Assign the point as the centroid.
                centroids[j] = X[idx]
                # Assign points to one of the centroids computed to this point.
                y = self.e(X,centroids)                
                print(f"y.head = {y[0:10,:]}")
                # Evaluate the inertia (euclidean distance) between ea point and its closest centroid.
                score = distance(X,y, centroid)
                print(f"    Score for this selection is {score}")
                # Save the current score and centroids
                trial_scores.append(score)
                trial_centroids[i,j,:]
        # Select start with lowest squared error between points
        # and their closest centroid
        best_idx = np.argmin(trial_scores)
        print(f"Best centroid selection was {best_idx} with a min score of {min(trial_scores)}")
        centroids = trial_centroids[best_idx,:,:]       
        
        return centroids

    def distance(X, y, centroids, metric="euclidean"):
        """Compute the sum of the euclidean distances between points and the centroid to which it is assigned."""
        if metric == "sse":
            result = np.sum(np.square(X.dot(y)-centroids),axis=1)
        else:
            result = np.sqrt(np.sum(np.square(X.dot(y)-centroids), axis=1))
        return result 

    def e(self, X, centroids):
        """Assign each point to its nearest centroid."""
        distances = cdist(X, centroids, 'euclidean')
        y = np.array([np.argmin(i) for i in distances])
        return y

    def m(self, X, y, centroids):
        """Recenter centroids to mean of the points assigned to each cluster."""
        centroids = y.T.dot(X)
        return centroids

    def fit(self, X):
        """Fits the k-means algorithm to the data."""

        dist_prev = np.inf
        self.centroids = self.initplusplus(X)
        for self.iter in range(self.max_iter):
            y = self.e(X, centroids)
            self.centroids = m(X, y, centroids)
            dist = distance(X,y,centroids)
            if np.abs(dist-dist_prev) < self.rtol:
                break
        self.labels = y.dot(self.cluster_labels)
        self.inertia = distance(X,y,centroids,"sse")
        return self

def main(infilepath, outfilepath):
    # Obtain the sequences as a list of lists
    io = IO()
    X = io.read(infilepath)
    print(f"X.shape is {X.shape}")
    kmeans = KMeans(k=3, n_init=10)
    kmeans.fit(X)

    # Write labels to output
    io.write(self.labels, outfilepath)

        
if __name__ == '__main__':
    infilepath = "../data/places.txt"
    outfilepath = "../data/clusters.txt"
    main(infilepath, outfilepath)

#%%    