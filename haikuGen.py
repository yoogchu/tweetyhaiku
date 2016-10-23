
import cPickle, random
# import twitbot.tweetbot
import bigramDictConstructor
import os

def constrained_sum_sample_pos(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""
    dividers = sorted(random.sample(xrange(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

def genLine(syllables, dictList):
    line = ""
    numWords = random.randint(1, syllables-2)  # determines the number of words to be built to fill out the required syllables
    if numWords == 1 and syllables > 5:  # to make sure not too many extremely long words are built
        numWords = random.randint(1, 2)
    syllLst = constrained_sum_sample_pos(numWords, syllables)

    for syllable in syllLst: # 1 in 3 chance for the syllable to be built from each of the dictionaries
        chance = random.randint(1, 3)
        if syllable > 1 and chance == 2:
            bgram = random.choice(dictList[1][syllable])
            line += bgram[0] + ' ' + bgram[1] + ' '
        elif syllable > 1 and chance == 3:
            try:
                bgram = random.choice(dictList[2][syllable])
            except IndexError:
                bgram = random.choice(dictList[1][syllable])
            line += bgram[0] + ' ' + bgram[1] + ' '
        else:
            line += random.choice(dictList[0][syllable]) + ' ' # always built from normal syllable dictionary if we need a 1 syllable word (no 1 syllable bigrams)
    return line + '\n'

def genHaiku(dictList):
    haiku = ""
    for num in [5, 7, 5]:
        haiku += genLine(num, dictList)
    return haiku # + "\n"

def main(word):
    file = open("syllableDict.txt", "rb")
    dict = cPickle.load(file) # loads the already created syllable dictionary consisting of 50,000+ words
    constructAss = bigramDictConstructor.getWord(word)

    file_name_brown = 'bigramDicts/' + word + '-brownBigramDict.txt'
    file_name_guten = 'bigramDicts/' + word + '-gutenbergBigramDict.txt'

    if constructAss is not None:
        brownBDict = cPickle.load(open(file_name_brown, "rb"))  # dictionary consisting of bigrams from the brown corpus
        gutenBDict = cPickle.load(open(file_name_guten, "rb")) # dictionary consisting of bigrams from the gutenberg corpus

        dictList = [dict, brownBDict, gutenBDict] # list of the dictionaries
        outFile = open("randomHaiku.txt", "w")

        return_haiku = genHaiku(dictList)

        print return_haiku
    else:
        return 'There was an error creating a haiku!'

def getWord(tweety_word):
    word = tweety_word
    print 'haikugen got: ' + word
    return main(word)


getWord('politics')
getWord('phones')
getWord('happy')
getWord('sad')
getWord('school')
getWord('shoes')
getWord('sword')
getWord('shirt')





