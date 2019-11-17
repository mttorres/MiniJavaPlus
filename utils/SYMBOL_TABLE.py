TABLE = {}


# tratar props (sempre deve ser uma lista de atributos)
# e tratar "entradas repetidas" (adicionar elas a lista de propriedades ou declarar erro?)
def insert(symbol,props):
    natabela = lookup(symbol)
    propstoadd = []
    if(type(props) != list):
        propstoadd.append(props)
    else:
        propstoadd = props

    if(type(natabela) != str):
        resolveconflict(natabela,propstoadd)

    TABLE[symbol] = propstoadd



def lookup(symbol):
    return TABLE.get(symbol,"NOT FOUND") # se nao encontra ele devolve NOT FOUND


def resolveconflict(tableentry,new):
    new.extend(tableentry) # por enquanto sempre adiciona a entrada (mais recente) nova a lista

def delete(symbol):
    return TABLE.pop(symbol,"NOT FOUND")






#insert("X",("int","x"))
#insert("X",("double","x"))
#print(TABLE)