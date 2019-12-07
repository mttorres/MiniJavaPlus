from utils.tree import Node
from utils.SYMBOL_TABLE import STable
from utils.TABLE_ENTRY import EntryProps

# percorrer o resto da arvore preenchendo(outros atributos sintetizados e herdados) o que nao da para ser feito na analise sintatica
# percorrer verficando  arvores (atributos herdados) tipos

#guardar também o endereço de memoria disponivel para todos eles ao guardar na tabela de simbolos!


MEMPOINTER = 0
METHODMEMPOINTER = 100
CLASSMEMPOINTER = 1000

def updateMemDisp():
    global MEMPOINTER
    MEMPOINTER += 1


def updateMethodMemDisp():
    global METHODMEMPOINTER
    METHODMEMPOINTER += 1

def updateClassMemDisp():
    global CLASSMEMPOINTER
    CLASSMEMPOINTER += 1

def novoEscopo(currentscope,tipo,iforder=None):
    ordem = len(currentscope.children)-1 if len(currentscope.children) > 0 else 0
    if(iforder != None):
        ordem = iforder

    basememoria = currentscope.defaultmem if tipo[0:6] != "metodo" else 100
    novoescopo = STable(tipo, order=ordem, level=currentscope.level + 1,defaultmem=basememoria)
    currentscope.assignchildren(novoescopo)
    currentscope = novoescopo
    return currentscope


def parameterCounter(globalscope,nomemetodo):
    # encontra o escopo
    escopoapropriado = None
    for escoposfilho in globalscope.children:
        if(escoposfilho.type == "metodo-"+nomemetodo ):
            escopoapropriado = escoposfilho
            break
    c =0
    for variaveis in escopoapropriado.TABLE:
        if(escopoapropriado.TABLE[variaveis].methodparam == True):
            c+=1

    return c


def constroiSymbT(node,atributos,currentscope):
    global MEMPOINTER
    global MEMPOINTER
    global CLASSMEMPOINTER
    # para qualquer insert na tabela de simbolos  salva para uma implementação mais sofisticada a posição de memoria disponivel

    #é a classe principal
    if(node.type == "prog"):
        # declara a classe principal
        if(currentscope.procupraNoAtualEnoExterno(node.leaf[1]) == "NOT_FOUND"):
            currentscope.insert(node.leaf[1],EntryProps(node.leaf[1],"CLASS-"+node.leaf[1],MEMPOINTER,currentscope))
            updateMemDisp()
        else:
            raise Exception("Erro: Declaração duplicada para a classe principal:  "+node.leaf[1])

        return list(filter(None,atributos))

    if(node.type == "main"):
        return list(filter(None, atributos))

    # declaração de variavel!
    if(node.type == "var"):
        if(currentscope.procupraNoAtualEnoExterno(node.leaf[0]) == "NOT_FOUND"):
            memoria = METHODMEMPOINTER if currentscope.type == "metodo" else MEMPOINTER
            currentscope.insert(node.leaf[0],EntryProps(node.leaf[0],atributos[0],memoria,currentscope))
            if(currentscope.type == "metodo"):
                updateMethodMemDisp()
            else:
                updateClassMemDisp()
        else:
            raise Exception("Declaração repetida da varíavel: "+node.leaf[0])

        return atributos[0]

    if(node.type == "tipo"):
        return node.leaf[0]



    if(node.type == "BNF-params"):
        if (len(atributos) == 1):
            return atributos[0]
        else:
            return list(filter(None, atributos))

    if(node.type == "params"):
        if (len(atributos) > 0 ):
            #deve declarar o parametro atual no escopo do metodo!
            currentscope.insert(node.leaf[0],
                                EntryProps(node.leaf[0], atributos[0] , METHODMEMPOINTER, currentscope,methodparam=True))
            updateMethodMemDisp()
            return atributos[0]
        else:
            return list(filter(None, atributos))

    if(node.type == "BNF-paramsExtra"):
        if(len(atributos) == 1):
            currentscope.insert(node.leaf[1],
                                EntryProps(node.leaf[1], atributos[0], METHODMEMPOINTER, currentscope,
                                           methodparam=True))
            updateMethodMemDisp()
            return atributos[0]
        else:
            return list(filter(None,atributos))

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
        if(node.leaf[1] == "="  and len(atributos) > 0):

            # não encontrou na tabela de simbolos
            encontrado = currentscope.procupraNoAtualEnoExterno(node.leaf[0])
            if(encontrado == "NOT_FOUND"):
                raise Exception("Variável "+node.leaf[0]+" não declarada!")


            # se ele encontrou na tabela de simbolos é porque é uma primeira atribuição ou atualização de valores
            # poderia em uma implementação mais sofisticada SALVAR O NOVO VALOR A POSIÇÃO DE MEMORIA PARA ADIANTAR A CGEN
            # mas para o escopo do trabalho ele só deve salvar O PRIMEIRO VALOR para realizar a cgen de forma mais facil
            else:
                if(encontrado.valor == None):
                    memoria = METHODMEMPOINTER if currentscope.type == "metodo" else MEMPOINTER
                    currentscope.insert(node.leaf[0], EntryProps(node.leaf[0], encontrado.tipo, memoria, currentscope,valor=atributos[0]))
                    if (currentscope.type == "metodo"):
                        updateMethodMemDisp()
                    else:
                        updateClassMemDisp()



        #pelo escopo desse trabalho ele só retorna o valor para o comando de cima (se necessário)
        #outro caso de atribuição é atribuição de vetores(nao usado nesse caso do trabalho)
        # duvida... retornar NONE ou atribuitos[0]? aparentemente nao faz diferença esse atributo não é usado por ninguem!
        return list(filter(None,atributos))

    # retorna as dependencias do if ou if e else
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
        if (len(atributos) == 0):
            return None

        if(len(atributos) == 1):
            return atributos[0]
        else:
            if (len(node.leaf) > 1):
                if (node.leaf[0] == "null" or node.leaf[1] == "null"):
                    raise Exception("NullPointerException")
            elif (len(node.leaf) > 0):
                if (node.leaf[0] == "null"):
                    raise Exception("NullPointerException")
                if(node.leaf[0] == '||'):
                    return (atributos[0] or atributos[1])
                if(node.leaf[0] == '&&'):
                    return (atributos[0] and atributos[1])

    if(node.type == "R-exp"):

        if (len(atributos) == 0):
            return None

        if(len(atributos) == 1):
            return atributos[0]
        else:
            if (len(node.leaf) > 1):
                if (node.leaf[0] == "null" or node.leaf[1] == "null"):
                    raise Exception("NullPointerException")
            elif(len(node.leaf) > 0):
                if (node.leaf[0] == "null"):
                    raise Exception("NullPointerException")
                if (node.leaf[0] == '=='):
                    return (atributos[0] == atributos[1])
                if (node.leaf[0] == '<'):
                    return (atributos[0] < atributos[1])
                if (node.leaf[0] == '!='):
                    return (atributos[0] != atributos[1])

    if(node.type == "A-exp"):

        if (len(atributos) == 0):
            return None

        if(len(atributos) == 1):
            return atributos[0]
        else:
            if (len(node.leaf) > 1):
                if (node.leaf[0] == "null" or node.leaf[1] == "null"):
                    raise Exception("NullPointerException")
            elif(len(node.leaf) > 0):
                if (node.leaf[0] == "null"):
                    raise Exception("NullPointerException")
                if (node.leaf[0] == '+'):
                    return (atributos[0] + atributos[1])
                if (node.leaf[0] == '-'):
                    return (atributos[0] - atributos[1])

    if(node.type =="M-exp"):

        if(len(atributos) == 0):
            return None

        if(len(atributos) == 1):
            return atributos[0]
        else:
            if(len(node.leaf) > 1):
                if (node.leaf[0] == "null" or node.leaf[1] == "null"):
                    raise Exception("NullPointerException")

            elif(len(node.leaf) > 0):
                if(node.leaf[0] == "null"):
                    raise Exception("NullPointerException")
                if (node.leaf[0] == '*'):
                    return (atributos[0] * atributos[1])
                if (node.leaf[0] == '/'):
                    return (atributos[0] // atributos[1])

    if(node.type == "S-exp"):
        # ele tem outro filho (nao é terminal)(ou seja o resultado é S-exp OPERAÇÃO S-exp ou outro não terminal
        if (len(node.children) != 0):
            if(len(atributos) != 0):

                if(len(node.leaf) > 0):
                    if(node.leaf[0] == "null"):
                        #vai realizar operação com NULL, erro!
                        raise Exception("NullPointerException")
                    if (node.leaf[0] == '!'):
                        return not(atributos[0])
                    if (node.leaf[0] == '-'):
                        return (-1)*(atributos[0])
                else:
                    return list(filter(None,atributos)) # é algo vindo de seu filho ainda (variavel ou algo mais)


        # PARTE MAIS IMPORTANTE (USO DE TERMINAIS)
        else:
            if(node.leaf[0] == "true"):
                return True
            if(node.leaf[0] == "false"):
                return False

            return node.leaf[0] # retorna null ou inteiro


    if (node.type == "P-exp"):
        # é variavel ( ou this) (mas this está fora do escopo dessa implementação)
        # esta usando essa variavel para, (ATRIBUIR NOVAMENTE, ATRIBUIR A PRIMEIRA VEZ OUTRA VARIAVEL, OU PARA OPERAÇÕES MATEMATICAS OU LOGICAS)
        # como na verdade ele verifica os casos de atribuição mais la em cima não é necessário verificar aqui tmb
        if(len(node.children) == 0 and len(node.leaf) > 0):
            if (node.leaf[0] == "new"):
                encontrado = currentscope.procupraNoAtualEnoExterno(node.leaf[1])
                if (encontrado == "NOT_FOUND"):
                    raise Exception("Classe" + node.leaf[1] + " não declarada!")
                else:
                    return None
            if(node.leaf[0] != "this"):
                encontrado = currentscope.procupraNoAtualEnoExterno(node.leaf[0])
                if(encontrado == "NOT_FOUND"):
                    raise Exception("Variável "+node.leaf[0]+" não foi  declarada!")
                else:
                    if(encontrado.valor == None  and encontrado.methodparam == False):
                        raise Exception("Variável " + node.leaf[0] + " não atribuida!")
                    return encontrado.valor # retorna o primeiro valor da variavel em P-exp ( para operações ou até uma atribuição lá em cima)

        # outros casos além de uso de variavel é o uso de : classes e metodos!
        # para o escopo desse trabalho só iremos verificar se essas classes e metodos estão declarados
        else:
            if(node.leaf[0] == "."):
                encontrado = currentscope.procupraNoAtualEnoExterno(node.leaf[1])
                if (encontrado == "NOT_FOUND"):
                    raise Exception("Método" + node.leaf[1] + " não declarada!")
                else:
                    #deve verificar se os parametros foram preenchidos !
                    #recuperar o metodo !
                    #contar quantos parametros ele tem!
                    if(encontrado.methodparam):
                        noparametros = parameterCounter(encontrado.parentScope, node.leaf[1])
                        if(noparametros != len(atributos)):
                            raise Exception("Método "+node.leaf[1]+" requer "+str(noparametros)+" parâmetro(s). "+str(len(atributos))+" foram preenchidos!")
                    return None




    if(node.type == "BNF-multiclass"):
        return list(filter(None,atributos))

    if(node.type == "classe"):
        if (currentscope.procupraNoAtualEnoExterno(node.leaf[1]) == "NOT_FOUND"):
            currentscope.insert(node.leaf[1], EntryProps(node.leaf[1], "CLASS-" + node.leaf[1], CLASSMEMPOINTER,currentscope))
            updateClassMemDisp()
        else:
            raise Exception("Erro: Classe " + node.leaf[1] + " já declarada!")
        return list(filter(None,atributos))



    # declaração de metodo
    if(node.type == "metodo"):
        return list(filter(None,atributos))

    if(node.type == "BNF-expOpcional"):
        return list(filter(None,atributos))

    if(node.type == "BNF-exps"):
        return list(filter(None,atributos))


def processTree(node,currentscope):
    if(node):

        # tratamento de escopo:
        if(node.type == "condstmt" and node.leaf[0] =="if"):
            currentscope = novoEscopo(currentscope,"if-condicional")
            currentscope.type = currentscope.type + str(currentscope.order)
        if (node.type == "matchornot" and node.leaf[0] == "else"):
            currentscope =  novoEscopo(currentscope.parent, "else-condicional",currentscope.order)

        if(node.type == "otherstmt" and len(node.leaf) != 0):
            if(node.leaf[0] == "while"):
                currentscope = novoEscopo(currentscope,"loop")
                currentscope.type = currentscope.type + str(currentscope.order)

        if(node.type == "metodo" and len(node.children) != 0):
            #declaração de metodo
            if (currentscope.procupraNoAtualEnoExterno(node.leaf[1]) == "NOT_FOUND"):
                temparametros = False
                if(node.children[1].type != "BNF-params"):
                    temparametros = True
                currentscope.insert(node.leaf[1],
                                    EntryProps(node.leaf[1], "MÉTODO-" + node.children[1].leaf[0], METHODMEMPOINTER, currentscope,methodparam=temparametros))
                updateMethodMemDisp()
                currentscope = novoEscopo(currentscope, "metodo-"+node.leaf[1])
            else:
                raise Exception("Erro: Método " + node.leaf[1] + " já declarado!")




        atributos_recuperados = []
        #resolve TODAS as dependencias do nó atual
        i = 0
        for child in node.children:


            #tratamento do escopo do else
            if(child.type == "cmd" and i == 0 and currentscope.type == "else-condicional"):
                currentscope.type = currentscope.type + str(currentscope.parent.children[currentscope.order-1].order)


            sint = processTree(child,currentscope)


            if(type(sint) == list):
                if(sint != None):
                    atributos_recuperados.extend(sint)
            else:
                if(sint != None):
                    atributos_recuperados.append(sint)
            i += 1

        #realiza ação semantica
        sint = constroiSymbT(node,atributos_recuperados,currentscope)

        return sint

    else:
        print("erro?")

