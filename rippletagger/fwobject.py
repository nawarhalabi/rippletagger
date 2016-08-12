# -*- coding: utf-8 -*-

class FWObject:
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
    def getFWObject(startWordTags, index):
        object = FWObject(True)
        word, tag = startWordTags[index]
        object.context[4] = word
        object.context[5] = tag

        decodedW = word
        if len(decodedW) >= 4:
            object.context[10] = decodedW[-2:]
            object.context[11] = decodedW[-3:]
        if len(decodedW) >= 5:
            object.context[12] = decodedW[-4:]

        if index > 0:
            preWord1, preTag1 = startWordTags[index - 1]
            object.context[2] = preWord1
            object.context[3] = preTag1

        if index > 1:
            preWord2, preTag2 = startWordTags[index - 2]
            object.context[0] = preWord2
            object.context[1] = preTag2

        if index < len(startWordTags) - 1:
            nextWord1, nextTag1 = startWordTags[index + 1]
            object.context[6] = nextWord1
            object.context[7] = nextTag1

        if index < len(startWordTags) - 2:
            nextWord2, nextTag2 = startWordTags[index + 2]
            object.context[8] = nextWord2
            object.context[9] = nextTag2

        return object

    def isSatisfied(self, fwObject):
        for i in xrange(13):
            key = self.context[i]
            if (key is not None):
                if key != fwObject.context[i]:
                    return False
        return True
