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
    d = {}
    for word in x.split(" "):
        d[word] = d.get(word, 0) + 1
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
    def predictor(x):
        f = featureExtractor(x)
        if dotProduct(weights, f) < 0.0:
            return -1
        else:
            return 1
    for i in range(numIters):
        for points in trainExamples:
            x, y = points
            f_x = featureExtractor(x)
            if dotProduct(weights, f_x) * y < 1.0: increment(weights, eta*y, f_x)
        print("Training Error:", evaluatePredictor(trainExamples, predictor))
        print("Test Error:", evaluatePredictor(testExamples, predictor))
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
        phi = {}
        for item in random.sample(weights.keys(), random.randint(1, len(weights))):
            phi[item] = random.randint(1, 30)
        if dotProduct(weights, phi) > 0.0: y = 1
        else: y = 0
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
        x = x.replace(" ", "")
        n_grams = [x[i:i+n] for i in range(len(x)- n + 1)]
        d = {}
        for item in n_grams:
            d[item] = d.get(item, 0) + 1
        return d
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
    centroids = [sample.copy() for sample in random.sample(examples, K)]
    keys = centroids[0].keys()
    def distance(centroids, point):
        l = [sum([(centroid[key] - point[key])**2 for key in centroid.keys()])**0.5 for centroid in centroids]
        return l.index(min(l)), sum(l)
    def update_centroids(assignments, centroids):
        for cluster in range(len(centroids)):
            for key in keys:
                centroids[cluster][key] = 0
            indices = [i for i, x in enumerate(assignments) if x == cluster]
            for indice in indices:
                point = examples[indice]
                for key in keys:
                    centroids[cluster][key] += point[key]
            for key in keys:
                if len(indices) != 0: centroids[cluster][key] /= len(indices)
        return centroids
    assignments = []
    for example in examples:
        assignment, loss = distance(centroids, example)
        assignments.append(assignment)
    for i in range(maxIters):
        centroids = update_centroids(assignments, centroids)
        past_assignment = assignments
        assignments = []
        for example in examples:
            assignment, loss = distance(centroids, example)
            assignments.append(assignment)
        if past_assignment == assignments:
            return centroids, assignments, loss
    return centroids, assignments, loss
    # END_YOUR_CODE

examples = generateClusteringExamples(10, 30, 20)
print(kmeans(examples, 5, 10))
