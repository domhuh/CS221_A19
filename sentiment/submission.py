#!/usr/bin/python

import random
import collections
import math
import sys
from util import *

############################################################
# Problem 3: binary classification
############################################################

############################################################
# Problem 3a: feature extraction

def extractWordFeatures(x):
    """
    Extract word features for a string x. Words are delimited by
    whitespace characters only.
    @param string x: 
    @return dict: feature vector representation of x.
    Example: "I am what I am" --> {'I': 2, 'am': 2, 'what': 1}
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    #raise Exception("Not implemented yet")
    d = {}
    for word in x.split(): d[word]=d.get(word,0)+1
    return d

    # END_YOUR_CODE

############################################################
# Problem 3b: stochastic gradient descent

def learnPredictor(trainExamples, testExamples, featureExtractor, numIters, eta):
    '''
    Given |trainExamples| and |testExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of iterations to
    train |numIters|, the step size |eta|, return the weight vector (sparse
    feature vector) learned.

    You should implement stochastic gradient descent.

    Note: only use the trainExamples for training!
    You should call evaluatePredictor() on both trainExamples and testExamples
    to see how you're doing as you learn after each iteration.
    '''
    weights = {}  # feature => weight
    # BEGIN_YOUR_CODE (our solution is 12 lines of code, but don't worry if you deviate from this)
    #raise Exception("Not implemented yet")

    for (x,y) in trainExamples:
        for word in x.split(): weights[word]=random.uniform(-0.1,0.1)
    for i in range(10):
        for x,y in trainExamples:
            feature = featureExtractor(x)
            prediction = dotProduct(weights,feature)
            scale = -eta * (prediction-y)
            increment(weights,scale,feature)

    # END_YOUR_CODE
    return weights

############################################################
# Problem 3c: generate test case

def generateDataset(numExamples, weights):
    '''
    Return a set of examples (phi(x), y) randomly which are classified correctly by
    |weights|.
    '''
    random.seed(42)
    # Return a single example (phi(x), y).
    # phi(x) should be a dict whose keys are a subset of the keys in weights
    # and values can be anything (randomize!) with a nonzero score under the given weight vector.
    # y should be 1 or -1 as classified by the weight vector.
    def generateExample():
        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
        #raise Exception("Not implemented yet")
        def sparseVectorDotProduct(v1, v2):
            allKeys = set([*list(v1.keys()), *list(v2.keys())])
            return sum([v1.get(e,0)*v2.get(e,0) for e in allKeys])
        phi = {}
        keys = random.choices(list(weights.keys()), k=random.randint(1,len(weights.keys())))
        for key in keys:
            phi[key] = random.randint(1,10)
        score = sparseVectorDotProduct(weights,phi)
        if score > 0: y = 1
        else: y = -1
        # END_YOUR_CODE
        return (phi, y)
    return [generateExample() for _ in range(numExamples)]

############################################################
# Problem 3e: character features

def extractCharacterFeatures(n):
    '''
    Return a function that takes a string |x| and returns a sparse feature
    vector consisting of all n-grams of |x| without spaces mapped to their n-gram counts.
    EXAMPLE: (n = 3) "I like tacos" --> {'Ili': 1, 'lik': 1, 'ike': 1, ...
    You may assume that n >= 1.
    '''
    def extract(x):
        # BEGIN_YOUR_CODE (our solution is 6 lines of code, but don't worry if you deviate from this)
        #raise Exception("Not implemented yet")
        grams = {}
        text = [c for c in x.replace(' ','')]
        for idx in range(len(text[:-n+1])): grams["".join(text[idx:idx+n])] = grams.get("".join(text[idx:idx+n]),0) + 1
        return grams
        # END_YOUR_CODE
    return extract

############################################################
# Problem 4: k-means
############################################################


def kmeans(examples, K, maxIters):
    '''
    examples: list of examples, each example is a string-to-double dict representing a sparse vector.
    K: number of desired clusters. Assume that 0 < K <= |examples|.
    maxIters: maximum number of iterations to run (you should terminate early if the algorithm converges).
    Return: (length K list of cluster centroids,
            list of assignments (i.e. if examples[i] belongs to centers[j], then assignments[i] = j)
            final reconstruction loss)
    '''
    # BEGIN_YOUR_CODE (our solution is 25 lines of code, but don't worry if you deviate from this)
    #raise Exception("Not implemented yet")
    def average(locs):
        avg = {}
        for loc in locs: increment(avg, 1 / float(len(locs)), loc)
        return avg
    def distance(loc1,loc2):
        dist = {}
        if len(loc1) < len(loc2): return distance(loc2, loc1)
        else:
            for k,v in loc1.items(): dist[k] = loc1[k] - loc2[k]
        return dotProduct(dist,dist)

    centroids = random.sample(examples,K)
#    assignments = []
#    flag = 0
    for _ in range(maxIters):
        assignmentVector = []
        for example in examples:
            cmin = sys.maxsize
            for n,centroid in enumerate(centroids):
                dist = distance(example, centroid)
                if dist<cmin: cmin,cargmin = dist, n
            assignmentVector.append(cargmin)
        centroids = [average([examples[p] for p,c in enumerate(assignmentVector) if c == n])
                                            for n, centroid in enumerate(centroids)]
#        for (a,b) in zip(assignments,assignmentVector):
#            if a!=b:
#                 flag = 0
#                 break
#             else: flag = 1
#         if flag: break
#         assignments = assignmentVector

    cost = 0
    for e,a in zip(examples, assignmentVector): cost += distance(e, centroids[a])

    return centroids, assignmentVector, cost
    # END_YOUR_CODE
