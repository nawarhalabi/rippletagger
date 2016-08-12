from codecs import open

class Node:
    """
    A node in a SCRDR tree
    """

    def __init__(
        self,
        feature,
        tag,
        father=None,
        exceptChild=None,
        elseChild=None,
        cornerstoneCases=[],
        depth=0,
    ):
        self.feature = feature
        self.tag = tag
        self.exceptChild = exceptChild
        self.elseChild = elseChild
        self.cornerstoneCases = cornerstoneCases
        self.father = father
        self.depth = depth

class FeatureVector:
    """
    A feature vector with features representing the context around a word
    """

    def __init__(self, initialize=False):
        self.prevWord2 = "<W>" if initialize else None   # 0
        self.prevTag2 = "<T>" if initialize else None    # 1
        self.prevWord1 = "<W>" if initialize else None   # 2
        self.prevTag1 = "<T>" if initialize else None    # 3
        self.word = "<W>" if initialize else None        # 4
        self.tag = "<T>" if initialize else None         # 5
        self.nextWord1 = "<W>" if initialize else None   # 6
        self.nextTag1 = "<T>" if initialize else None    # 7
        self.nextWord2 = "<W>" if initialize else None   # 8
        self.nextTag2 = "<T>" if initialize else None    # 9
        self.suffixL2 = "<SFX>" if initialize else None  # 10
        self.suffixL3 = "<SFX>" if initialize else None  # 11
        self.suffixL4 = "<SFX>" if initialize else None  # 12

    def matches(self, other):
        return (
            (other.prevWord2 is None or self.prevWord2 == other.prevWord2) and
            (other.prevTag2 is None or self.prevTag2 == other.prevTag2) and
            (other.prevWord1 is None or self.prevWord1 == other.prevWord1) and
            (other.prevTag1 is None or self.prevTag1 == other.prevTag1) and
            (other.word is None or self.word == other.word) and
            (other.tag is None or self.tag == other.tag) and
            (other.nextWord1 is None or self.nextWord1 == other.nextWord1) and
            (other.nextTag1 is None or self.nextTag1 == other.nextTag1) and
            (other.nextWord2 is None or self.nextWord2 == other.nextWord2) and
            (other.nextTag2 is None or self.nextTag2 == other.nextTag2) and
            (other.suffixL2 is None or self.suffixL2 == other.suffixL2) and
            (other.suffixL3 is None or self.suffixL3 == other.suffixL3) and
            (other.suffixL4 is None or self.suffixL4 == other.suffixL4)
        )

    def set_key(self, key, value):
        self.__dict__[key] = value

    @staticmethod
    def getFeatureVector(tagged_sentence, index):
        feature = FeatureVector(True)
        word, tag = tagged_sentence[index]
        feature.word = word
        feature.tag = tag

        if len(word) >= 4:
            feature.suffixL2 = word[-2:]
            feature.suffixL3 = word[-3:]

        if len(word) >= 5:
            feature.suffixL4 = word[-4:]

        if index > 0:
            feature.prevWord1, feature.prevTag1 = tagged_sentence[index - 1]

        if index > 1:
            feature.prevWord2, feature.prevTag2 = tagged_sentence[index - 2]

        if index < len(tagged_sentence) - 1:
            feature.nextWord1, feature.nextTag1 = tagged_sentence[index + 1]

        if index < len(tagged_sentence) - 2:
            feature.nextWord2, feature.nextTag2 = tagged_sentence[index + 2]

        return feature

class SCRDRTree:
    """
    Single Classification Ripple Down Rules tree for Part-of-Speech and morphological tagging
    """

    def __init__(self, root=None):
        self.root = root

    # Build tree from file containing rules using FeatureVector
    def constructSCRDRtreeFromRDRfile(self, rulesFilePath):
        self.root = Node(FeatureVector(False), "NN", None, None, None, [], 0)
        currentNode = self.root
        currentDepth = 0

        rulesFile = open(rulesFilePath, "r", encoding="utf-8")
        lines = rulesFile.readlines()

        for i in xrange(1, len(lines)):
            line = lines[i]
            depth = 0
            for c in line:
                if c == '\t':
                    depth = depth + 1
                else:
                    break

            line = line.strip()
            if len(line) == 0:
                continue

            temp = line.find("cc")
            if temp == 0:
                continue

            condition, conclusion = line.split(" : ", 1)
            feature = self.getFeature(condition.strip())
            tag = self.getTag(conclusion.strip())

            node = Node(feature, tag, None, None, None, [], depth)

            if depth > currentDepth:
                currentNode.exceptChild = node
            elif depth == currentDepth:
                currentNode.elseChild = node
            else:
                while currentNode.depth != depth:
                    currentNode = currentNode.father
                currentNode.elseChild = node

            node.father = currentNode
            currentNode = node
            currentDepth = depth

    def findFiredNode(self, feature):
        currentNode = self.root
        firedNode = None
        while True:
            # Check whether object satisfying the current node's feature
            satisfied = feature.matches(currentNode.feature)

            if satisfied:
                firedNode = currentNode
                exChild = currentNode.exceptChild
                if exChild is None:
                    break
                else:
                    currentNode = exChild
            else:
                elChild = currentNode.elseChild
                if elChild is None:
                    break
                else:
                    currentNode = elChild
        return firedNode

    def getTag(self, str):
        if str.find('""') > 0:
            if str.find("Word") > 0:
                return "<W>"
            elif str.find("suffixL") > 0:
                return "<SFX>"
            else:
                return "<T>"
        return str[str.find("\"") + 1: len(str) - 1]

    def getFeature(self, condition):
        feature = FeatureVector(False)
        for rule in condition.split(" and "):
            rule = rule.strip()
            key = rule[rule.find(".") + 1: rule.find(" ")]
            value = self.getTag(rule)
            feature.set_key(key, value)

        return feature
