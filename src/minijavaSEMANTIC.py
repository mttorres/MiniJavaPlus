from utils.tree import Node
from utils.SYMBOL_TABLE import STable
from utils.TABLE_ENTRY import EntryProps

# percorrer o resto da arvore preenchendo(outros atributos sintetizados e herdados) o que nao da para ser feito na analise sintatica
# percorrer verficando  arvores (atributos herdados) tipos

#guardar também o endereço de memoria disponivel para todos eles ao guardar na tabela de simbolos!


MEMPOINTER = 0
METHODMEMPOINTER = 100
CLASSMEMPOINTER = 500

def updateMemDisp():
    global MEMPOINTER
    MEMPOINTER += 1


def updateMethodMemDisp():
    global METHODMEMPOINTER
    METHODMEMPOINTER += 1

def updateClassMemDisp():
    global CLASSMEMPOINTER
    CLASSMEMPOINTER += 1

def novoEscopo(currentscope,tipo):
    novoescopo = STable(tipo, order=currentscope.order + 1, level=currentscope.level + 1)
    currentscope.assignchildren(novoescopo)
    currentscope = novoescopo
    return currentscope


def constroiSymbT(node,atributos,currentscope):
    global MEMPOINTER
    global MEMPOINTER
    global CLASSMEMPOINTER
    # para qualquer insert na tabela de simbolos  salva para uma implementação mais sofisticada a posição de memoria disponivel

    #é a classe principal
    if(node.type == "prog"):
        if(currentscope.procupraNoAtualEnoExterno(node.leaf[1]) == "NOT_FOUND"):
            currentscope.insert(node.leaf[1],EntryProps(node.leaf[1],"CLASS-"+node.leaf[1],MEMPOINTER,currentscope))
            updateMemDisp()
        else:
            raise Exception("Erro: Declaração duplicada para a classe principal:  "+node.leaf[1])


    if(node.type == "var"):
        if(currentscope.procupraNoAtualEnoExterno(node.leaf[0]) == "NOT_FOUND"):
            currentscope.insert(node.leaf[0],EntryProps(node.leaf[0],atributos[0],MEMPOINTER,currentscope))
            updateMemDisp()
        else:
            raise Exception("Declaração repetida da varíavel: "+node.leaf[0])

    if(node.type == "tipo"):
        return node.leaf[0]

    if(node.type == "BNF-cmd"):
        if(len(atributos) == 1):
            return atributos[0]
        else:
            return list(filter(None,atributos))

    # só pode ser condicional ou other (comandos(blocos), while, SOUT, atribuição)
    # # no fim das contas... ele vai descendo (bloco dentro de bloco) e pode atribuir ou dar print no final!
    # ou seja repassa as dependencias para o nó mais acima
    if(node.type == "cmd"):
        if(len(atributos) == 1):
            return atributos[0]
        else:
            return list(filter(None,atributos))


    # todos esses só tem um atributo de verdade para passar para o seu pai (o exp) que deve ter a dependencia resolvida!
    if(node.type == "otherstmt"):
        if(len(atributos) == 1):
            return atributos[0]
        else:
            return list(filter(None,atributos))


    #salvar na tabela de simbolos (possivelmente a primeira atribuição) (ou reatribuição)
    if(node.type == "assignment"):
        #atribuição de variavel
        # tem só um atributo(recuperado de EXP via recursão)
        if(node.leaf[1] == "=" ):
            tipo = type(atributos[0])
            if (tipo == bool):
                tipo = "booleano"
            else:
                tipo = "int"
            if(currentscope.procupraNoAtualEnoExterno(node.leaf[0]) == "NOT_FOUND"):
                currentscope.insert(node.leaf[0],EntryProps(node.leaf[0], tipo, MEMPOINTER, currentscope))
                updateMemDisp()

            # se ele encontrou na tabela de simbolos é porque é uma reatribuição ou atualização de valores
            # poderia em uma implementação mais sofisticada SALVAR O NOVO VALOR A POSIÇÃO DE MEMORIA PARA ADIANTAR A CGEN
            #mas para o escopo do trabalho ele só deve salvar O PRIMEIRO VALOR para realizar a cgen de forma mais facil
            else:
                if(currentscope.procupraNoAtualEnoExterno(node.leaf[0]).valor == None):
                    currentscope.insert(node.leaf[0], EntryProps(node.leaf[0], tipo, MEMPOINTER, currentscope,valor=atributos[0]))
                    updateMemDisp()



        #pelo escopo desse trabalho ele só retorna o valor para o comando de cima (se necessário)
        #outro caso de atribuição é atribuição de vetores(nao usado nesse caso do trabalho)
        # duvida... retornar NONE ou atribuitos[0]?
        return atributos[0]

    # retorna as dependencias do if ou if e else
    # entramos em um novo escopo
    if(node.type == "condstmt"):
        if(len(atributos) == 1):
            return atributos[0]
        else:
            return list(filter(None,atributos))

    # mesma coisa de antes
    if(node.type == "matchornot"):
        if(len(atributos) == 1):
            return atributos[0]
        else:
            return list(filter(None,atributos))


    # EXP (talvez o caso mais importante (substituir valores imediatos e declarações!)
    if(node.type == "exp"):
        if(len(atributos) == 1):
            return atributos[0]
        else:
            if (node.children[0] == "null" or node.children[1] == "null"):
                raise Exception("NullPointerException")

            if(node.children[0] == '||'):
                return (atributos[0] or atributos[1])
            if(node.children[0] == '&&'):
                return (atributos[0] and atributos[1])

    if(node.type == "R-exp"):
        if(len(atributos) == 1):
            return atributos[0]
        else:
            if (node.children[0] == "null" or node.children[1] == "null"):
                raise Exception("NullPointerException")

            if (node.children[0] == '=='):
                return (atributos[0] == atributos[1])
            if (node.children[0] == '<'):
                return (atributos[0] < atributos[1])
            if (node.children[0] == '!='):
                return (atributos[0] != atributos[1])

    if(node.type == "A-exp"):
        if(len(atributos) == 1):
            return atributos[0]
        else:
            if (node.children[0] == "null" or node.children[1] == "null"):
                raise Exception("NullPointerException")
            if (node.children[0] == '+'):
                return (atributos[0] + atributos[1])
            if (node.children[0] == '-'):
                return (atributos[0] - atributos[1])

    if(node.type =="M-exp"):
        if(len(atributos) == 1):
            return atributos[0]
        else:
            if (node.children[0] == "null" or node.children[1] == "null"):
                raise Exception("NullPointerException")

            if (node.children[0] == '*'):
                return (atributos[0] * atributos[1])
            if (node.children[0] == '/'):
                return (atributos[0] / atributos[1])

    if(node.type == "S-exp"):

        if (len(node.children) != 0):
            if(node.children[0] == "null"):
                raise Exception("NullPointerException")
            if (node.children[0] == '!'):
                return not(atributos[0])
            if (node.children[0] == '-'):
                return (-1)*(atributos[0])

        # PARTE MAIS IMPORTANTE (USO DE TERMINAIS)(OU DE VARIAVEIS)
        else:
            # é uma variavel!
            if((node.leaf[0] != "null")  and (type(node.leaf[0]) != bool and type(node.leaf[0]) != int )):
                if (currentscope.procupraNoAtualEnoExterno(node.leaf[0]) == "NOT_FOUND"):
                    raise Exception("Variável "+node.leaf[0]+" não declarada!")
                else:
                    return currentscope.procupraNoAtualEnoExterno(node.leaf[0]).value
            else:
                return node.leaf[0]


    #if (node.type == "P-exp"):
        #if()








    if(node.type == "classe"):
        if (currentscope.procupraNoAtualEnoExterno(node.leaf[1]) == "NOT_FOUND"):
            currentscope.insert(node.leaf[1], EntryProps(node.leaf[1], "CLASS-" + node.leaf[1], CLASSMEMPOINTER,currentscope))
            updateClassMemDisp()
        else:
            raise Exception("Erro: Classe " + node.leaf[1] + " já declarada!")
        return atributos


    # declaração de metodo
    if(node.type == "metodo"):
        if(currentscope.procupraNoAtualEnoExterno(node.leaf[1]) == "NOT_FOUND"):
            currentscope.insert(node.leaf[1], EntryProps(node.leaf[1], "MÉTODO-" + atributos[0], METHODMEMPOINTER ,currentscope))
            updateMethodMemDisp()
            novoEscopo(currentscope, "metodo")
        else:
            raise Exception("Erro: Método " + node.leaf[1] + " já declarado!")

        return atributos

    return "nada por enquanto"










def processTree(node,currentscope):
    if(node):
        #novoescopo = STable("if",order=currentscope.order+1,level=currentscope.level+1)
        #currentscope.assignchildren(novoescopo)
        #currentscope = novoescopo
        #while
        #metodo
        #classe?

        # tratamento de escopo:
        if(node.type == "condstmt"):
            novoEscopo(currentscope,"condicional")

        if(node.type == "otherstmt" and len(node.children) != 0):
            if(node.children[0] == "while"):
                novoEscopo(currentscope,"loop")





        atributos_recuperados = []
        #resolve TODAS as dependencias do nó atual
        for child in node.children:
            sint = processTree(child,currentscope)
            atributos_recuperados.append(sint)

        #realiza ação semantica
        sint =constroiSymbT(node,atributos_recuperados,currentscope)

        return sint
    else:
        print("erro?")

