# -*- coding: utf-8 -*-

from learner.tagger_initial import initializeSentence
from learner.tree import SCRDRTree
from learner.fwobject import FWObject
from learner.utils import readDictionary

class Tagger(SCRDRTree):
    def __init__(self, model_path):
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

r = Tagger("Models/UniPOS/UD_French/train.UniPOS")
print r.tag(u"Cette annonce a fait l' effet d' une véritable bombe .")

r = Tagger("Models/UniPOS/UD_Swedish/train.UniPOS")
print r.tag(u"Fördomen har alltid sin rot i vardagslivet")
