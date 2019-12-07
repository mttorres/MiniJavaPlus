BLOCK_CONTROL = 0


class Node:
    def __init__(self,nodetype,children=None,leaf=None,lineno=None):
        self.type = nodetype
        if children:
            self.children = list(filter(None, children))
        else:
            self.children = [ ]
        if leaf:
            self.leaf = list(filter(None, leaf))
        else:
            self.leaf = [ ]

        self.lineno = lineno

    def __str__(self):
        return "[NODE]: %s" % (self.type)

    def pretty(self,file = None):
        i = 0
        #print("[NODE]: %s  - %d children - %d tokens" % (self.type, len(self.children), len(self.leaf)))
        #print("\t[TOKENS]: %s" % (self.leaf))
        if(file):
           writeNode(self,file)
        while i < len(self.children):
            #print("\t[CHILD #%d]: %s\n" % (i, self.children[i]))
            if(file):
                writeChild(self,file,i)
                self.children[i].pretty(file)
            else:
                self.children[i].pretty()
            i += 1






    def cgen(self,Table):
        global BLOCK_CONTROL
        nodeName = self.type
        tokens = self.leaf
        children = self.children

        # print(nodeName)
        # print(tokens)
        # for child in children: print(child)
        # print('')

        if(nodeName == 'prog'):
            print("-- Begin MIPS code")
            print("\tb main")
            children[0].cgen(Table)
            children[1].cgen(Table)
        if(nodeName == "main"):
            print("main:")
            children[0].cgen(Table)
        elif(nodeName == "BNF-multiclass"):
            children[0].cgen(Table)
        elif(nodeName == 'classe'):
            children[0].cgen(Table)
        elif(nodeName == 'BNF-metodo'):
            children[0].cgen(Table)
        elif(nodeName == 'metodo'):
            # definição de metodo
            # encontra o escopo apropriado(DEVIA TER SALVO OS FILHOS DOS ESCOPOS EM OUTRA TABELA HASH?)
            for escoposfilho in Table.children:
                if(escoposfilho.type == ("metodo-"+tokens[1])):
                    Table = escoposfilho
                    break
            # deve  realizar algumas manipulações de memoria e avaliar o CORPO DA FUNÇÃO
            print("%s:" % tokens[1])
            print("\tmove $fp $sp")
            sw('ra',0,'sp')
            addiu('sp','sp',-4)
            children[2].cgen(Table)
            children[3].cgen(Table)

            # desempilha a expressao da função !
            lw('ra',4,'sp')
            # DESEMPILHAR PARAMETROS  e  TODAS AS VARIAVEIS LOCAIS
            addiu('sp','sp',(4*len(Table.TABLE))+8)
            lw('fp',0,'sp')
            print("\tjr $ra")
            #devolve o controle de bloco para zero ao desempilhar (sair do metodo)
            if(BLOCK_CONTROL > 0):
                BLOCK_CONTROL = 0


        elif(nodeName == 'BNF-cmd'):
            children[0].cgen(Table)
        elif(nodeName == "cmd"):
            children[0].cgen(Table)
        elif(nodeName == "otherstmt"):
            if(len(tokens) == 0):
                children[0].cgen(Table)
            else:
                # é print (guarda em a0 para fazer algo com isso (ex: tratar como string o resultado)
                if(tokens[0] == "System.out.println"):
                    # ao fim da função ComputeFac ele guarda o ULTIMO VALOR EM a0 ou seja...
                    # podemos simplesmente... chamar a função e então computar o valor em a0
                    children[0].cgen(Table)
                # é o while
                else:
                    for escoposfilho in Table.children:
                        if (escoposfilho.type == ("if-condicional" + str(BLOCK_CONTROL))):
                            Table = escoposfilho
                            break

                    #avaliar expressão
                    print("WHILE-COND:")
                    children[0].cgen(Table) # ao final ela vai ter 1 como resultado
                    print("\tbgtz $a0 WHILE-LOOP") # se for 1 pula para o loop
                    print("\tj LOOP-EXIT") # senao vai para a saida

                    #operacoes do while
                    print("WHILE-LOOP:")
                    children[1].cgen(Table)
                    print("\tj WHILE-COND") # reavalia a expressão
                    print("LOOP-EXIT: ")


                    # desempilhar bloco
                    if (BLOCK_CONTROL > 0):
                        BLOCK_CONTROL = 0

        elif(nodeName == "condstmt"):
            #chamar o enesimo if dentro do escopo atual com COND_STMT_CONTROL
            for escoposfilho in Table.children:
                if(escoposfilho.type == ("if-condicional"+str(BLOCK_CONTROL))):
                    Table = escoposfilho
                    break
            # avaliar a expressao do if
            children[0].cgen(Table)
            children[1].cgen(Table)

        elif(nodeName == "matchornot"):
            #comprar se é 0 ou 1 (usar branc on greater than zero)
            print("\tbgtz $a0 true_if")
            print('else_label:')
            if (len(children) > 1):
                for escoposfilho in Table.parent.children:
                    if (escoposfilho.type == ("else-condicional" + str(BLOCK_CONTROL))):
                        Table = escoposfilho
                        break
                children[1].cgen(Table)
            print("\tb end_if")

            print('true_if:')
            children[0].cgen(Table)

            print("end_if:")

            BLOCK_CONTROL+=1


        # atribuição de variaveis
        elif(nodeName == 'assignment'):
            # o equivalente de x = 1 é :  li $a0 1  ou  lw $a0 (memoria) !? (DEPENDE!) se ele vier de uma variavel sim!
            # o que fazer? x = algo (exp) ( exp pode ser variavel, imediato ou combinação deles!)
            # 2 escolhas... garantir que o valor esteja na pilha (ai é só carregar de 0sp)
            # garantir que o valor esteja seja calculado isto é ao desempilhar a recursao do cgen ele retorna SEMPRE um imediato!
            # se o valor for uma composição de variaveis ou imediatos (expressão) (deve ter que recuperar da pilha também..)

            if tokens[1] == '=':
                expressaoavaliada = children[0].cgen(Table)
                #valor retornado é imediato(veio direto de um nó terminal)
                if(expressaoavaliada != "$a0"):
                    print('\tli $a0 %s' % str(expressaoavaliada))
                #senao for terminal ele já carrega o valor de a0 em memoria normalmente (nenhuma ação é necessária!)
            # caso de vetores (precisa fazer?)
            else:
                print('\tli $a0 %s' % children[1].cgen(Table))
            #salvar (lembrando que as operacoes devem sempre mudar e voltar com o estado da pilha)
            #nesse caso nao deve pq ele vai utilizar essas variaveis(?)
            sw('a0', 0, 'sp')
            addiu('sp','sp',-4)

        elif (nodeName == 'exp'):
            #é cgen(expressaoNAOTERMINAL) ou cgen(e1 logical/aritimetico e2)
            if(tokens):
                children[0].cgen(Table) # lembrando que ao fim de cada cgen(e) ele salva em a0
                sw('a0', 0, 'sp')
                addiu('sp', 'sp', -4)
                children[1].cgen(Table)
                lw('t1',4,'sp')
                if(tokens[0] == '&&'):
                    print('\tand $a0 $t1 $a0')
                elif(tokens[0] == '||'):
                    print('\tor $a0 $t1 $a0')
                addiu('sp', 'sp', 4) # manter o estado da pilha(desempilhar o valor carregado em t1)

                return "$a0" # retornar para o comando pai "saber oque fazer" e onde esta o dado procurado

            else:
                return children[0].cgen(Table)

        elif(nodeName == 'R-exp'):
            if(tokens):
                children[0].cgen(Table)
                sw('a0', 0, 'sp')
                addiu('sp', 'sp', -4)
                children[1].cgen(Table)
                lw('t1', 4, 'sp')
                if(tokens[0] == '<'):
                    print('\tslt $a0 $t1 $a0')
                elif(tokens[0] == '=='):
                    print('\tbeq $t1 $a0 equal')
                    print('equal:')
                    print("\tli $a0 1")

                elif(tokens[0] == '!='):
                    print('\tbne $a0 $t1 not_equal')
                    print("\tli $a0 0")

                addiu('sp', 'sp', 4)  # manter o estado da pilha(desempilhar o valor carregado em t1)
                return "$a0"

            else:
                return children[0].cgen(Table)
        elif(nodeName == 'A-exp'):
            if(tokens):
                children[0].cgen(Table)
                sw('a0', 0, 'sp')
                addiu('sp', 'sp', -4)
                children[1].cgen(Table)
                lw('t1', 4, 'sp')
                if(tokens[0] == '+'):
                    print('\tadd $a0 $t1 $a0')
                elif(tokens[0] == '-'):
                    print('\tsub $a0 $t1 $a0')
                addiu('sp','sp',4)

                return "$a0"

            else:
                return children[0].cgen(Table)

        elif(nodeName == 'M-exp'):
            if(tokens):
                children[0].cgen(Table)
                sw('a0', 0, 'sp')
                addiu('sp', 'sp', -4)
                children[1].cgen(Table)
                lw('t1', 4, 'sp')
                if(tokens[0] == '*'):
                    print('\tmult $a0 $t1 $a0')
                elif(tokens[0] == '/'):
                    print('\tdiv $a0 $t1 $a0')
                addiu('sp','sp',4)

                return "$a0"
            else:
                return children[0].cgen(Table)
        elif(nodeName == 'S-exp'):
            # imediatos ( ou terminais) (on ainda variaveis !)
            if(tokens):
                if(type(tokens[0]) == int):
                    return str(tokens[0])
                elif(tokens[0] == 'false'):
                    return 0
                elif(tokens[0] == 'true'):
                    return 1
                elif(tokens[0] == '-'):
                    return ('-' + children[0].cgen(Table))
            else:
                return children[0].cgen(Table)

        elif(nodeName == 'P-exp'):
            # chamada de metodo ou uso de variavel
            # se uma expressao usa uma variavel (é pq ela ja foi declarada e atribuida, ou teria quebrado na analise semantica!)
            # ou seja ela ESTÁ NA PILHA ! (foi salva em memoria)
            # já que QUALQUER OPERAÇÃO ou expressão executada antes de avaliar P-exp deve manter o estado da pilha IGUAL a antes dela
            # a variavel que desejamos já declarada está exatamente na ultima posição + um offset !
            # OQUE FAZER? recuperar da pilha com esse offset--> a TABELA DE SIMBOLOS GUARDA A POSIÇÃO EM MEMÓRIA DAS VARIAVEIS!

            if(len(children) == 0):
                # é a variavel ou this!
                if(tokens[0] != "this"):
                    var = Table.procupraNoAtualEnoExterno(tokens[0])
                    if(var != "NOT_FOUND"):
                        # eu salvei como sendo memlocation = 0,1,...n
                        # logo o offset é:
                        offset = 4 + (var.memlocation/Table.defaultmem)*4
                        # ex: primeira declaração 4 + 4*0
                        # ex: segunda declaração 4 + 4*1 ...
                        lw('a0',offset,'sp')
                        return "$a0"
                    else:
                        raise Exception("Não foi possível ler a varíavel  %s da tabela de simbolos!",tokens[0])


            else:
                if(tokens[0] == "."):
                    sw('fp', 0, 'sp')
                    addiu('sp', 'sp', -4)
                    # chamada de metodos com parametros
                    if(len(children) > 1):
                        children[1].cgen(Table)

                        pass
                    # sem parametros
                    else:
                        pass
                    print("\tjal %s" % tokens[1])
                else:
                    # ou não encontrou os parametros ainda
                    children[0].cgen(Table)

        elif(nodeName == "BNF-expOpicional"):
            children[0].cgen(Table)
        elif(nodeName == "BNF-exps"):
            # tem mais de um parametro
            if(len(children) > 1):
                children[1].cgen(Table)
            # avaliacao em ordem reversa
            children[0].cgen(Table)
            sw('a0',0,'sp')
            addiu('sp','sp',-4)
        elif(nodeName == "BNF-expList"):
            #avaliacao em ordem reversa
            if(len(children)> 1):
                children[0].cgen(Table)
            children[1].cgen(Table)
            sw('a0', 0, 'sp')
            addiu('sp', 'sp', -4)


# metodos auxiliares
            
def writeNode(self,file):
    file.write("[NODE]: %s  - %d children - %d tokens" % (self.type, len(self.children), len(self.leaf)))
    file.write("\n")
    file.write("\t[TOKENS]: %s" % (self.leaf))
    file.write("\n")


def writeChild(self,file,i):
    file.write("\t[CHILD #%d]: %s\n" % (i, self.children[i]))
    file.write("\n")

def addiu(acc, register, amt):
    print('\taddiu $%s $%s %d' % (acc, register, amt))

def sw(source, offset, register):
    print('\tsw $%s %d($%s)' % (source, offset, register))

def lw(register,offset,source):
    print("\tlw $%s %d($%s)" %(register,offset,source))