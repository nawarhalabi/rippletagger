# -*- coding: utf-8 -*-

import re

from rippletagger.models import SCRDRTree, FeatureVector
from rippletagger.utils import readDictionary

class Tagger(SCRDRTree):
    def __init__(self, language):
        mapper = LanguageMapper()
        directory_name = mapper.directory_name(language)
        model_path = "Models/UD_%s/train.UniPOS" % directory_name

        self.constructSCRDRtreeFromRDRfile(model_path + ".RDR")
        self.DICT = readDictionary(model_path + ".DICT")

    def tag(self, line):
        tagger = FrequencyTagger(self.DICT)
        guessed_tags = tagger.tag(line)
        sentence = []

        for i, guessed_tag in enumerate(guessed_tags):
            feature = FeatureVector.getFeatureVector(guessed_tags, i)
            node = self.findFiredNode(feature)
            word, tag = guessed_tag

            sentence.append((word, node.conclusion if node.depth > 0 else tag))

        return sentence

class FrequencyTagger:
    def __init__(self, FREQDICT):
        self.FREQDICT = FREQDICT

    def tag(self, line):
        words = line.strip().split()
        taggedSen = []
        for word in words:
            if word in [u"“", u"”", u"\""]:
                taggedSen.append("''/" + self.FREQDICT["''"])
                continue

            tag = ''
            decodedW = word
            lowerW = decodedW.lower()
            if word in self.FREQDICT:
                tag = self.FREQDICT[word]
            elif lowerW in self.FREQDICT:
                tag = self.FREQDICT[lowerW]
            else:
                if re.search(r"[0-9]+", word) is not None:
                    tag = self.FREQDICT["TAG4UNKN-NUM"]
                else:
                    suffixL2 = suffixL3 = suffixL4 = suffixL5 = None
                    wLength = len(decodedW)
                    if wLength >= 4:
                        suffixL3 = ".*" + decodedW[-3:]
                        suffixL2 = ".*" + decodedW[-2:]
                    if wLength >= 5:
                        suffixL4 = ".*" + decodedW[-4:]
                    if wLength >= 6:
                        suffixL5 = ".*" + decodedW[-5:]

                    if suffixL5 in self.FREQDICT:
                        tag = self.FREQDICT[suffixL5]
                    elif suffixL4 in self.FREQDICT:
                        tag = self.FREQDICT[suffixL4]
                    elif suffixL3 in self.FREQDICT:
                        tag = self.FREQDICT[suffixL3]
                    elif suffixL2 in self.FREQDICT:
                        tag = self.FREQDICT[suffixL2]
                    elif decodedW[0].isupper():
                        tag = self.FREQDICT["TAG4UNKN-CAPITAL"]
                    else:
                        tag = self.FREQDICT["TAG4UNKN-WORD"]

            taggedSen.append((word, tag))

        return taggedSen

class LanguageMapper:
    def __init__(self):
        with open("models/language_mapping.txt", "r") as f:
            mapping_lines = [line.strip() for line in f.readlines()]

        language_twocode = {}
        language_threecode = {}
        language_name = {}

        for line in mapping_lines:
            if line.startswith("#") or not line.strip():
                continue

            twocode, threecode, name, directory_name = line.split(", ")
            language_twocode[twocode] = directory_name.strip()
            language_threecode[threecode] = directory_name.strip()
            language_name[name] = directory_name

        self.language_twocode = language_twocode
        self.language_threecode = language_threecode
        self.language_name = language_name

    def directory_name(self, code_or_name):
        if code_or_name in self.language_twocode:
            return self.language_twocode[code_or_name]
        elif code_or_name in self.language_threecode:
            return self.language_threecode[code_or_name]
        elif code_or_name in self.language_name:
            return self.language_name[code_or_name]

        raise Exception(
            "Language '%s' not found. See models/language_mapping.txt"
            " for valid language codes" % code_or_name
        )

    def all_language_codes(self):
        return self.language_threecode.keys()
