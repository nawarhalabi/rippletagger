# -*- coding: utf-8 -*-

from rippletagger.tagger_initial import initializeSentence
from rippletagger.tree import SCRDRTree
from rippletagger.fwobject import FWObject
from rippletagger.utils import readDictionary

class Tagger(SCRDRTree):
    def __init__(self, language):
        mapper = LanguageMapper()
        directory_name = mapper.directory_name(language)
        model_path = "Models/UD_%s/train.UniPOS" % directory_name

        self.constructSCRDRtreeFromRDRfile(model_path + ".RDR")
        self.DICT = readDictionary(model_path + ".DICT")

    def tag(self, line):
        guessed_tags = initializeSentence(self.DICT, line.encode("utf-8"))
        sentence = []

        for i, guessed_tag in enumerate(guessed_tags):
            fwObject = FWObject.getFWObject(guessed_tags, i)
            word, tag = guessed_tag
            node = self.findFiredNode(fwObject)

            sentence.append((word, node.conclusion if node.depth > 0 else tag))

        return sentence

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
