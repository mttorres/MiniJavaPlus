from utils.tree import Node
from utils.SYMBOL_TABLE import STable
from utils.TABLE_ENTRY import EntryProps

# percorrer o resto da arvore preenchendo(outros atributos sintetizados e herdados) o que nao da para ser feito na analise sintatica
# percorrer verficando  arvores (atributos herdados) tipos

#guardar também o endereço de memoria disponivel para todos eles ao guardar na tabela de simbolos!

TABLE_POINTER = []
MEMPOINTER = 0

def updateMemDisp():
    global MEMPOINTER
    MEMPOINTER += 1

def constroiSymbT(node,atributos):
    global TABLE_POINTER
    global MEMPOINTER
    if(node.type == "prog"):
        escopoglobal = STable()
        TABLE_POINTER.append(escopoglobal)
        if(escopoglobal.lookup(node.leaf[1]) == "NOT_FOUND"):
            escopoglobal.insert(node.leaf[1],EntryProps(node.leaf[1],"CLASS-"+node.leaf[1],MEMPOINTER,escopoglobal))
            updateMemDisp()
        else:
            raise Exception("Erro: Classe "+node.leaf[1]+" já declarada!")

    if(node.type == "classe"):
        if (TABLE_POINTER[0].lookup(node.leaf[1]) == "NOT_FOUND"):
            MEMPOINTER = 100
            TABLE_POINTER[0].insert(node.leaf[1], EntryProps(node.leaf[1], "CLASS-" + node.leaf[1], MEMPOINTER,escopoglobal))
            updateMemDisp()
        else:
            raise Exception("Erro: Classe " + node.leaf[1] + " já declarada!")

    if(node.type == "metodo"):
        if(TABLE_POINTER[0].lookup(node.leaf[1]) == "NOT_FOUND"):
            escopoLocal = STable()
            TABLE_POINTER[0].insert(node.leaf[1], EntryProps(node.leaf[1], "MÉTODO-" + node.children[0].leaf[0], MEMPOINTER,escopoLocal))
            updateMemDisp()
            TABLE_POINTER[0].assignchildren(escopoLocal)
        else:
            raise Exception("Erro: Método " + node.leaf[1] + " já declarado!")










#TODO : PENSAR NUMA FORMA MELHOR E MAIS SIMPLES DE : SALVAR DECLARAÇÕES E VALORES DELAS


def processTree(node):
    if(node):
        atributos_recuperados = []
        for child in node.children:
            atributos_recuperados.append(processTree(node))

        #veificaTipos (poderia fazer no metodo de construir SymbolT?)(como descer a arvore e devolver o tipo da declaração PAI?)
        # no enunciado ele nao pede tipos... FOCAR SÓ EM VERIFICAR DECLARAÇÕES!
        # e também só em gerar código
        # OU SEJA NECESSITAMOS DE : SALVAR DECLARAÇÕES E VALORES

        constroiSymbT(node,atributos_recuperados)


        if(len(node.leaf) == 1):
            return node.lef[0]

    else:
        print("erro?")

