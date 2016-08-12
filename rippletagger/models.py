from codecs import open

class Node:
    """
    A node in a SCRDR tree
    """

    def __init__(
        self,
        feature,
        conclusion,
        father=None,
        exceptChild=None,
        elseChild=None,
        cornerstoneCases=[],
        depth=0,
    ):
        self.feature = feature
        self.conclusion = conclusion
        self.exceptChild = exceptChild
        self.elseChild = elseChild
        self.cornerstoneCases = cornerstoneCases
        self.father = father
        self.depth = depth

class FeatureVector:
    """
    A feature vector with features representing the context around a word
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

            feature = self.getFeature(line.split(" : ", 1)[0].strip())
            conclusion = self.getConcreteValue(line.split(" : ", 1)[1].strip())

            node = Node(feature, conclusion, None, None, None, [], depth)

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
        obContext = feature.context
        while True:
            # Check whether object satisfying the current node's feature
            cnContext = currentNode.feature.context
            satisfied = True
            for i in xrange(13):
                if (cnContext[i] is not None):
                    if cnContext[i] != obContext[i]:
                        satisfied = False
                        break

            if(satisfied):
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

    def getConcreteValue(self, str):
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
            value = self.getConcreteValue(rule)

            if key == "prevWord2":
                feature.context[0] = value
            elif key == "prevTag2":
                feature.context[1] = value
            elif key == "prevWord1":
                feature.context[2] = value
            elif key == "prevTag1":
                feature.context[3] = value
            elif key == "word":
                feature.context[4] = value
            elif key == "tag":
                feature.context[5] = value
            elif key == "nextWord1":
                feature.context[6] = value
            elif key == "nextTag1":
                feature.context[7] = value
            elif key == "nextWord2":
                feature.context[8] = value
            elif key == "nextTag2":
                feature.context[9] = value
            elif key == "suffixL2":
                feature.context[10] = value
            elif key == "suffixL3":
                feature.context[11] = value
            elif key == "suffixL4":
                feature.context[12] = value

        return feature
