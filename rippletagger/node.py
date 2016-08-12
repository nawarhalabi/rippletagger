class Node:
    """
    A class to represent the nodes in SCRDR tree
    """

    def __init__(
        self, condition, conclusion, father=None, exceptChild=None,
        elseChild=None, cornerstoneCases=[], depth=0
    ):
        self.condition = condition
        self.conclusion = conclusion
        self.exceptChild = exceptChild
        self.elseChild = elseChild
        self.cornerstoneCases = cornerstoneCases
        self.father = father
        self.depth = depth
