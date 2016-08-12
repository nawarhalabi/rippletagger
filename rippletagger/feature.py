# -*- coding: utf-8 -*-

class FeatureVector:
    """
    RDRPOSTaggerV1.1: new implementation scheme
    RDRPOSTaggerV1.2: add suffixes
    """

    def __init__(self, check=False):
        self.context = [None, None, None, None, None, None, None, None, None, None, None, None, None]
        if check:
            i = 0
            while (i < 10):
                self.context[i] = "<W>"
                self.context[i + 1] = "<T>"
                i = i + 2
            self.context[10] = "<SFX>"  # suffix
            self.context[11] = "<SFX>"
            self.context[12] = "<SFX>"

    @staticmethod
    def getFeatureVector(startWordTags, index):
        feature = FeatureVector(True)
        word, tag = startWordTags[index]
        feature.context[4] = word
        feature.context[5] = tag

        decodedW = word
        if len(decodedW) >= 4:
            feature.context[10] = decodedW[-2:]
            feature.context[11] = decodedW[-3:]
        if len(decodedW) >= 5:
            feature.context[12] = decodedW[-4:]

        if index > 0:
            preWord1, preTag1 = startWordTags[index - 1]
            feature.context[2] = preWord1
            feature.context[3] = preTag1

        if index > 1:
            preWord2, preTag2 = startWordTags[index - 2]
            feature.context[0] = preWord2
            feature.context[1] = preTag2

        if index < len(startWordTags) - 1:
            nextWord1, nextTag1 = startWordTags[index + 1]
            feature.context[6] = nextWord1
            feature.context[7] = nextTag1

        if index < len(startWordTags) - 2:
            nextWord2, nextTag2 = startWordTags[index + 2]
            feature.context[8] = nextWord2
            feature.context[9] = nextTag2

        return feature
