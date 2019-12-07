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






    def cgen(self,Table,outputfile):
        global BLOCK_CONTROL
        nodeName = self.type
        tokens = self.leaf
        children = self.children

        # print(nodeName)
        # print(tokens)
        # for child in children: print(child)
        # print('')

        if(nodeName == 'prog'):
            outputfile.write("-- Begin MIPS code\n")
            outputfile.write("\tb main\n")
            children[0].cgen(Table,outputfile)
            children[1].cgen(Table,outputfile)
        if(nodeName == "main"):
            outputfile.write("main:\n")
            children[0].cgen(Table,outputfile)
        elif(nodeName == "BNF-multiclass"):
            children[0].cgen(Table,outputfile)
        elif(nodeName == 'classe'):
            children[0].cgen(Table,outputfile)
        elif(nodeName == 'BNF-metodo'):
            children[0].cgen(Table,outputfile)
        elif(nodeName == 'metodo'):
            # definição de metodo
            # encontra o escopo apropriado(DEVIA TER SALVO OS FILHOS DOS ESCOPOS EM OUTRA TABELA HASH?)
            for escoposfilho in Table.children:
                if(escoposfilho.type == ("metodo-"+tokens[1])):
                    Table = escoposfilho
                    break
            # deve  realizar algumas manipulações de memoria e avaliar o CORPO DA FUNÇÃO
            outputfile.write("%s:\n" % tokens[1])
            outputfile.write("\tmove $fp $sp\n")
            sw('ra',0,'sp',outputfile)
            addiu('sp','sp',-4,outputfile)
            children[2].cgen(Table,outputfile)
            children[3].cgen(Table,outputfile)

            # desempilha a expressao da função !
            lw('ra',4,'sp',outputfile)
            # DESEMPILHAR PARAMETROS  e  TODAS AS VARIAVEIS LOCAIS
            addiu('sp','sp',(4*len(Table.TABLE))+8,outputfile)
            lw('fp',0,'sp',outputfile)
            outputfile.write("\tjr $ra\n")
            #devolve o controle de bloco para zero ao desempilhar (sair do metodo)
            if(BLOCK_CONTROL > 0):
                BLOCK_CONTROL = 0


        elif(nodeName == 'BNF-cmd'):
            children[0].cgen(Table,outputfile)
        elif(nodeName == "cmd"):
            children[0].cgen(Table,outputfile)
        elif(nodeName == "otherstmt"):
            if(len(tokens) == 0):
                children[0].cgen(Table,outputfile)
            else:
                # é print (guarda em a0 para fazer algo com isso (ex: tratar como string o resultado)
                if(tokens[0] == "System.out.println"):
                    # ao fim da função ComputeFac ele guarda o ULTIMO VALOR EM a0 ou seja...
                    # podemos simplesmente... chamar a função e então computar o valor em a0
                    children[0].cgen(Table,outputfile)
                # é o while
                else:
                    for escoposfilho in Table.children:
                        if (escoposfilho.type == ("if-condicional" + str(BLOCK_CONTROL))):
                            Table = escoposfilho
                            break

                    #avaliar expressão
                    outputfile.write("WHILE-COND: \n")
                    children[0].cgen(Table,outputfile) # ao final ela vai ter 1 como resultado
                    outputfile.write("\tbgtz $a0 WHILE-LOOP\n") # se for 1 pula para o loop
                    outputfile.write("\tj LOOP-EXIT\n") # senao vai para a saida

                    #operacoes do while
                    outputfile.write("WHILE-LOOP: \n")
                    children[1].cgen(Table,outputfile)
                    outputfile.write("\tj WHILE-COND\n") # reavalia a expressão
                    outputfile.write("LOOP-EXIT: \n")


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
            children[0].cgen(Table,outputfile)
            children[1].cgen(Table,outputfile)

        elif(nodeName == "matchornot"):
            #comprar se é 0 ou 1 (usar branc on greater than zero)
            outputfile.write("\tbgtz $a0 true_if\n")
            outputfile.write('else_label: \n')
            if (len(children) > 1):
                for escoposfilho in Table.parent.children:
                    if (escoposfilho.type == ("else-condicional" + str(BLOCK_CONTROL))):
                        Table = escoposfilho
                        break
                children[1].cgen(Table,outputfile)
            outputfile.write("\tb end_if \n")

            outputfile.write('true_if: \n')
            children[0].cgen(Table,outputfile)

            outputfile.write("end_if: \n")

            BLOCK_CONTROL+=1


        # atribuição de variaveis
        elif(nodeName == 'assignment'):
            # o equivalente de x = 1 é :  li $a0 1  ou  lw $a0 (memoria) !? (DEPENDE!) se ele vier de uma variavel sim!
            # o que fazer? x = algo (exp) ( exp pode ser variavel, imediato ou combinação deles!)
            # 2 escolhas... garantir que o valor esteja na pilha (ai é só carregar de 0sp)
            # garantir que o valor esteja seja calculado isto é ao desempilhar a recursao do cgen ele retorna SEMPRE um imediato!
            # se o valor for uma composição de variaveis ou imediatos (expressão) (deve ter que recuperar da pilha também..)

            if tokens[1] == '=':
                expressaoavaliada = children[0].cgen(Table,outputfile)
                #valor retornado é imediato(veio direto de um nó terminal)
                if(expressaoavaliada != "$a0"):
                    outputfile.write('\tli $a0 %s\n' % str(expressaoavaliada))
                #senao for terminal ele já carrega o valor de a0 em memoria normalmente (nenhuma ação é necessária!)
            # caso de vetores (precisa fazer?)
            else:
                outputfile.write('\tli $a0 %s\n' % children[1].cgen(Table,outputfile))
            #salvar (lembrando que as operacoes devem sempre mudar e voltar com o estado da pilha)
            #nesse caso nao deve pq ele vai utilizar essas variaveis(?)
            sw('a0', 0, 'sp',outputfile)
            addiu('sp','sp',-4,outputfile)

        elif (nodeName == 'exp'):
            #é cgen(expressaoNAOTERMINAL) ou cgen(e1 logical/aritimetico e2)
            if(tokens):
                children[0].cgen(Table,outputfile) # lembrando que ao fim de cada cgen(e) ele salva em a0
                sw('a0', 0, 'sp',outputfile)
                addiu('sp', 'sp', -4,outputfile)
                children[1].cgen(Table,outputfile)
                lw('t1',4,'sp',outputfile)
                if(tokens[0] == '&&'):
                    outputfile.write('\tand $a0 $t1 $a0\n')
                elif(tokens[0] == '||'):
                    outputfile.write('\tor $a0 $t1 $a0\n')
                addiu('sp', 'sp', 4,outputfile) # manter o estado da pilha(desempilhar o valor carregado em t1)

                return "$a0" # retornar para o comando pai "saber oque fazer" e onde esta o dado procurado

            else:
                return children[0].cgen(Table,outputfile)

        elif(nodeName == 'R-exp'):
            if(tokens):
                children[0].cgen(Table,outputfile)
                sw('a0', 0, 'sp',outputfile)
                addiu('sp', 'sp', -4,outputfile)
                children[1].cgen(Table,outputfile)
                lw('t1', 4, 'sp',outputfile)
                if(tokens[0] == '<'):
                    outputfile.write('\tslt $a0 $t1 $a0\n')
                elif(tokens[0] == '=='):
                    outputfile.write('\tbeq $t1 $a0 equal\n')
                    outputfile.write('equal: \n')
                    outputfile.write("\tli $a0 1 \n")

                elif(tokens[0] == '!='):
                    outputfile.write('\tbne $a0 $t1 not_equal\n')
                    outputfile.write("\tli $a0 0\n")

                addiu('sp', 'sp', 4,outputfile)  # manter o estado da pilha(desempilhar o valor carregado em t1)
                return "$a0"

            else:
                return children[0].cgen(Table,outputfile)
        elif(nodeName == 'A-exp'):
            if(tokens):
                children[0].cgen(Table,outputfile)
                sw('a0', 0, 'sp',outputfile)
                addiu('sp', 'sp', -4,outputfile)
                children[1].cgen(Table,outputfile)
                lw('t1', 4, 'sp',outputfile)
                if(tokens[0] == '+'):
                    outputfile.write('\tadd $a0 $t1 $a0\n')
                elif(tokens[0] == '-'):
                    outputfile.write('\tsub $a0 $t1 $a0\n')
                addiu('sp','sp',4,outputfile)

                return "$a0"

            else:
                return children[0].cgen(Table,outputfile)

        elif(nodeName == 'M-exp'):
            if(tokens):
                children[0].cgen(Table,outputfile)
                sw('a0', 0, 'sp',outputfile)
                addiu('sp', 'sp', -4,outputfile)
                children[1].cgen(Table,outputfile)
                lw('t1', 4, 'sp',outputfile)
                if(tokens[0] == '*'):
                    outputfile.write('\tmult $a0 $t1 $a0\n')
                elif(tokens[0] == '/'):
                    outputfile.write('\tdiv $a0 $t1 $a0\n')
                addiu('sp','sp',4,outputfile)

                return "$a0"
            else:
                return children[0].cgen(Table,outputfile)
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
                    return ('-' + children[0].cgen(Table,outputfile))
            else:
                return children[0].cgen(Table,outputfile)

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
                        lw('a0',offset,'sp',outputfile)
                        return "$a0"
                    else:
                        raise Exception("Não foi possível ler a varíavel  %s da tabela de simbolos!",tokens[0])


            else:
                if(tokens[0] == "."):
                    sw('fp', 0, 'sp',outputfile)
                    addiu('sp', 'sp', -4,outputfile)
                    # chamada de metodos com parametros
                    if(len(children) > 1):
                        children[1].cgen(Table,outputfile)
                    # sem parametros
                    else:
                        pass
                    outputfile.write("\tjal %s\n" % tokens[1])
                else:
                    # ou não encontrou os parametros ainda
                    children[0].cgen(Table,outputfile)

        elif(nodeName == "BNF-expOpicional"):
            children[0].cgen(Table,outputfile)
        elif(nodeName == "BNF-exps"):
            # tem mais de um parametro
            if(len(children) > 1):
                children[1].cgen(Table,outputfile)
            # avaliacao em ordem reversa
            children[0].cgen(Table,outputfile)
            sw('a0',0,'sp',outputfile)
            addiu('sp','sp',-4,outputfile)
        elif(nodeName == "BNF-expList"):
            #avaliacao em ordem reversa
            if(len(children)> 1):
                children[0].cgen(Table,outputfile)
            children[1].cgen(Table,outputfile)
            sw('a0', 0, 'sp',outputfile)
            addiu('sp', 'sp', -4,outputfile)


# metodos auxiliares
            
def writeNode(self,file):
    file.write("[NODE]: %s  - %d children - %d tokens" % (self.type, len(self.children), len(self.leaf)))
    file.write("\n")
    file.write("\t[TOKENS]: %s" % (self.leaf))
    file.write("\n")


def writeChild(self,file,i):
    file.write("\t[CHILD #%d]: %s\n" % (i, self.children[i]))
    file.write("\n")

def addiu(acc, register, amt,outputfile):
    outputfile.write('\taddiu $%s $%s %d\n' % (acc, register, amt))

def sw(source, offset, register,outputfile):
    outputfile.write('\tsw $%s %d($%s)\n' % (source, offset, register))

def lw(register,offset,source,outputfile):
    outputfile.write("\tlw $%s %d($%s)\n" %(register,offset,source))