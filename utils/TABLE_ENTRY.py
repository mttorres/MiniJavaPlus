NEXT_MEM_LOC = 0


class EntryProps:
    def __init__(self, name, memlocation, parentScope,linenumber,pos):
        #por enquanto isso teremos esses atributos
        self.name = name
        self.memlocation = memlocation
        self.parentScope = parentScope
        self.linenumber = linenumber
        self.post = pos