
import nltk.corpus
import nltk.collocations
import collections
import cPickle
from collections import defaultdict
import wordassociate as wordAssociate
import os.path

def bigramFinder(wordAssList, text):
    """Returns a list of popular bigrams from a corpus"""

    bgm = nltk.collocations.BigramAssocMeasures()

    bigramLst = []

    print 'finding relevant bigrams ...'

    for x in wordAssList:
        if text == 0:
            finder = nltk.collocations.BigramCollocationFinder.from_words(nltk.corpus.brown.words())
        elif text == 1:
            finder = nltk.collocations.BigramCollocationFinder.from_words(nltk.corpus.gutenberg.words())
        finder.apply_ngram_filter(lambda *w: x not in w)
        finder.apply_freq_filter(3) # must be found at least 3 times
        bigrams = finder.nbest(bgm.pmi, 10000)

        for i in range(len(bigrams)):
            valid = True
            for j in range(2):
                if bigrams[i][j] in [",", ".", "!", '"']: # must not contain punctuation
                    valid = False
            if valid:
                bigramLst.append(bigrams[i])
                print bigramLst

    return bigramLst

def bigramDict(dictionary, bigramLst):
    """Assigns bigram pairs to correct syllable count in a dictionary"""

    bDict = defaultdict(list)
    for i in range(len(bigramLst)):
        syllSum = 0
        bgm = []
        for j in range(2):
            key = [key for key,value in dictionary.items() if bigramLst[i][j].lower() in value] # finds each word in the bigram in the already created syllable dict
            if key != []:
                syllSum += key[0] # if found, adds the correct number of syllables to the syllable sum for that bigram
                bgm.append(str(bigramLst[i][j]).lower()) # appends that part of the bigram to a list for that bigram
        if len(bgm) == 2 and syllSum <= 7: # if the bigram is full (meaning that both parts passed through the syllable check) adds the list to the list in the bigram dictionary
            bDict[syllSum].append(bgm)
    return bDict

def main(word, wordAssList):
    file = open("syllableDict.txt", "rb")
    dict = cPickle.load(file) # loads the already created syllable dictionary

    file_name_brown = 'bigramDicts/' + word + '-brownBigramDict.txt'
    file_name_guten = 'bigramDicts/' + word + '-gutenbergBigramDict.txt'    

    if not os.path.isfile(file_name_brown):
        bDict = bigramDict(dict, bigramFinder(wordAssList, 0))
        print 'populating brown ...'
        cPickle.dump(bDict, open(file_name_brown, "wb")) # saves brown bigram dictionary

    if not os.path.isfile(file_name_guten):
        bDict = bigramDict(dict, bigramFinder(wordAssList, 1))
        print 'populating gutenberg ...'
        cPickle.dump(bDict, open(file_name_guten, "wb")) # saves gutenberg bigram dictionary

    print 'done'
    return True

def getWord(tweetyword):
    word = tweetyword
    wordAssList = wordAssociate.getResponse(word)
    print wordAssList

    if wordAssList is not None:
        return main(word, wordAssList)
    else:
        return None
