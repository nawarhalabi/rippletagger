# -*- coding: utf-8 -*-

from codecs import open

def readDictionary(inputFile):
    dictionary = {}
    lines = open(inputFile, "r", encoding="utf-8").readlines()
    for line in lines:
        wordtag = line.strip().split()
        dictionary[wordtag[0]] = wordtag[1]
    return dictionary
