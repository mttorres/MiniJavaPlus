class STable:
    # tratar props (sempre deve ser uma lista de atributos)(definir quais atributos por default!) (criei outra classe TABLE_ENTRY
    # e tratar "entradas repetidas" (adicionar elas a lista de propriedades ou declarar erro?)
    def __init__(self,type="Global",parent = None, order = 0, level = 0):
        self.parent = parent
        self.children = []
        self.order = order
        self.type = type
        self.level = level
        self.TABLE = {}
        # até agora imagino que ele va utilizar essas propriedades

    def insert(self,symbol,props):
        if(type(symbol) != str or type(symbol) == STable):
            print("estou criando outro escopo dentro desse")
            self.children = symbol
            symbol.parent = self

        natabela = self.lookup(symbol)


        self.TABLE[symbol] = props

    def __str__(self):
        if(self.parent):
            paistr = "\t"+str(self.TABLE)
        else:
            paistr = str(self.TABLE)


        if (self.children):
            if(self.parent):
                paistr += "\n\tFILHOS:\n\t"+str(self.order)+"*"
            else:
                paistr += "\nFILHOS:\n"+str(self.order)+"*"
            for c in self.children:
                filhostr =  c.__str__()
                paistr += filhostr
            paistr += "  "+str(self.order)+"*"
        return paistr

    def lookup(self,symbol):
        return self.TABLE.get(symbol,"NOT_FOUND") # se nao encontra ele devolve NOT FOUND

    def procupraNoAtualEnoExterno(self,symbol):
        resultado = self.lookup(symbol)
        pai = self.parent
        while(pai and resultado == "NOT_FOUND"):
            resultado = pai.lookup(symbol)
            pai = pai.parent
        return resultado

    def resolveconflict(self,tableentry,new):
        new.extend(tableentry) # por enquanto sempre adiciona a entrada (mais recente) nova a lista

    def delete(self,symbol):
        return self.TABLE.pop(symbol,"NOT_FOUND")

    def assignchildren(self,other):
        self.children.append(other)
        other.parent = self


'''
t1 = STable(None,1)
t1.insert("X",("int","x"))
t1.insert("X",("double","x"))
t1.insert("Y",("int","Y"))
t1.insert("Y",("double","Y"))
t1.insert("Z",("int","Z"))
t1.insert("Z",("double","Z"))
print(t1)

t2 = STable(None,2,"While")
t3 = STable(None,3,"if")
t4 = STable(None,4,"if")
t5 = STable(None,5,"if")
t6 = STable(None,6,"if")

t2.insert("cond",("boolean","true"))
t2.insert("C",("int","0"))

t3.insert("cond",("boolean","true"))
t3.insert("z",("int","2"))

t4.insert("cond",("boolean","true"))
t4.insert("z",("int","3"))

t5.insert("cond",("boolean","true"))
t5.insert("z",("int","4"))

t6.insert("cond",("boolean","true"))
t6.insert("z",("int","6"))


t1.assignchildren(t2)

t2.assignchildren(t3)
t2.assignchildren(t4)
t2.assignchildren(t5)

t3.assignchildren(t6)

print()
#print(t1.delete("Z"))
#print(t1.delete("Z"))
print(t1)

#print(type(t1))
'''