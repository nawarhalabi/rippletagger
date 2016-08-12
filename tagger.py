# -*- coding: utf-8 -*-

from SCRDRlearner.SCRDRTree import SCRDRTree
from SCRDRlearner.Object import FWObject
from learner.tagger_initial import initializeSentence
from learner.utils import readDictionary

class RDRPOSTagger(SCRDRTree):
    def __init__(self, model_path):
        self.constructSCRDRtreeFromRDRfile(model_path + ".RDR")
        self.DICT = readDictionary(model_path + ".DICT")

    def tagRawSentence(self, line):
        guessed_tags = initializeSentence(self.DICT, line.encode("utf-8"))
        sentence = []

        for i, guessed_tag in enumerate(guessed_tags):
            fwObject = FWObject.getFWObject(guessed_tags, i)
            word, tag = guessed_tag
            node = self.findFiredNode(fwObject)

            sentence.append((word, node.conclusion if node.depth > 0 else tag))

        return sentence

r = RDRPOSTagger("Models/UniPOS/UD_French/train.UniPOS")
print r.tagRawSentence(u"Cette annonce a fait l' effet d' une véritable bombe .")

r = RDRPOSTagger("Models/UniPOS/UD_Swedish/train.UniPOS")
print r.tagRawSentence(u"Fördomen har alltid sin rot i vardagslivet")
