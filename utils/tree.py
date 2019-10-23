class Node:
    def __init__(self,type,children=None,leaf=None):
        self.type = type
        if children:
            self.children = list(filter(None, children))
        else:
            self.children = [ ]
        if leaf:
            self.leaf = list(filter(None, leaf))
        else:
            self.leaf = [ ]

    def __str__(self):
        return "[NODE]: %s" % (self.type)

    def pretty(self):
        i = 0
        print("[NODE]: %s  - %d children - %d tokens" % (self.type, len(self.children), len(self.leaf)))
        print("\t[TOKENS]: %s" % (self.leaf))
        while i < len(self.children):
            print("\t[CHILD #%d]: %s\n" % (i, self.children[i]))
            self.children[i].pretty()
            i += 1