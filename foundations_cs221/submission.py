import collections
import math

############################################################
# Problem 3a

def findAlphabeticallyLastWord(text):
    """
    Given a string |text|, return the word in |text| that comes last
    alphabetically (that is, the word that would appear last in a dictionary).
    A word is defined by a maximal sequence of characters without whitespaces.
    You might find max() and list comprehensions handy here.
    """
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    return max(text.split())
    # END_YOUR_CODE

############################################################
# Problem 3b

def euclideanDistance(loc1, loc2):
    """
    Return the Euclidean distance between two locations, where the locations
    are pairs of numbers (e.g., (3, 5)).
    """
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    return (abs(loc2[0]-loc1[0])**2 + abs(loc2[1]-loc1[1])**2)**0.5
    # END_YOUR_CODE

############################################################
# Problem 3c

def mutateSentences(sentence):
    """
    Given a sentence (sequence of words), return a list of all "similar"
    sentences.
    We define a sentence to be similar to the original sentence if
      - it as the same number of words, and
      - each pair of adjacent words in the new sentence also occurs in the original sentence
        (the words within each pair should appear in the same order in the output sentence
         as they did in the orignal sentence.)
    Notes:
      - The order of the sentences you output doesn't matter.
      - You must not output duplicates.
      - Your generated sentence can use a word in the original sentence more than
        once.
    Example:
      - Input: 'the cat and the mouse'
      - Output: ['and the cat and the', 'the cat and the mouse', 'the cat and the cat', 'cat and the cat and']
                (reordered versions of this list are allowed)
    """
    # BEGIN_YOUR_CODE (our solution is 20 lines of code, but don't worry if you deviate from this)
    if " " in sentence: words = sentence.split(" ")
    else: words = sentence
    print(sentence, "===============")
    if len(words) <= 3:
        return [sentence]
    d = {}
    similarSentences = []
    for i, word in enumerate(words):
        if i != len(words) - 1: d[word] = d.get(word, []) + [words[i+1]]
    for i in d:
        d[i] = list(set(d[i]))
    def recurse(s):
        sentences = []
        if len(s) == len(words):
            return [s]
        if len(s) < len(words):
            for pair in d.get(s[-1], []):
                sentences += recurse(s + [pair])
            return sentences
        else:
            for pair in d.get(s[-1]):
                print(pair)
                sentences += recurse(s + [pair])
            return sentences
    for word in d:
        similarSentences += recurse([word])
    answer = []
    for sentence in similarSentences:
        answer.append(" ".join(sentence))
    return answer
    # END_YOUR_CODE

############################################################
# Problem 3d

def sparseVectorDotProduct(v1, v2):
    """
    Given two sparse vectors |v1| and |v2|, each represented as collections.defaultdict(float), return
    their dot product.
    You might find it useful to use sum() and a list comprehension.
    This function will be useful later for linear classifiers.
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    keys = [i for i in v1]
    dot_list = [v1[key]*v2[key] for key in keys]
    return sum(dot_list)
    # END_YOUR_CODE

############################################################
# Problem 3e

def incrementSparseVector(v1, scale, v2):
    """
    Given two sparse vectors |v1| and |v2|, perform v1 += scale * v2.
    This function will be useful later for linear classifiers.
    """
    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
    keys = [j for j in v2 if j not in v1] + [i for i in v1]
    for i in keys:
        v1[i] += scale * v2[i]
    return v1
    # END_YOUR_CODE

############################################################
# Problem 3f

def findSingletonWords(text):
    """
    Splits the string |text| by whitespace and returns the set of words that
    occur exactly once.
    You might find it useful to use collections.defaultdict(int).
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    d = {}
    for word in text.split():
        d[word] = d.get(word, 0) + 1
    return set([i for i in d.keys() if d[i] == 1])
    # END_YOUR_CODE

############################################################
# Problem 3g

def computeLongestPalindromeLength(text):
    """
    A palindrome is a string that is equal to its reverse (e.g., 'ana').
    Compute the length of the longest palindrome that can be obtained by deleting
    letters from |text|.
    For example: the longest palindrome in 'animal' is 'ama'.
    Your algorithm should run in O(len(text)^2) time.
    You should first define a recurrence before you start coding.
    """
    # BEGIN_YOUR_CODE (our solution is 19 lines of code, but don't worry if you deviate from this)
    cache = {}
    def recurse(text):
        if text in cache: cost = cache[text]
        elif len(text) <= 1: cost = 0
        elif text[0] == text[-1]:
            if len(text) == 2: cost = 0
            else: cost = recurse(text[1:-1])
        else:
            rightCost = 1 + recurse(text[:-1])
            leftCost = 1 + recurse(text[1:])
            cost = min(rightCost, leftCost)
        if text not in cache: cache[text] = cost
        return cost
    return len(text) - recurse(text)
    # END_YOUR_CODE