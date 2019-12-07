
class EntryProps:
    def __init__(self, name, tipo, memlocation,parentScope,valor=None,methodparam=None):
        #por enquanto isso teremos esses atributos
        self.name = name
        self.tipo = tipo
        self.memlocation = memlocation
        self.valor = valor
        self.methodparam= methodparam
        self.parentScope = parentScope