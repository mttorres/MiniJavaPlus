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

    def cgen(self):
        nodeName = self.type
        tokens = self.leaf
        children = self.children
        # print(nodeName)
        # print(tokens)
        # for child in children: print(child)
        # print('')
        if(nodeName == 'prog'):
            print("-- Begin MIPS code")
            children[0].cgen()
            children[1].cgen()
        elif(nodeName == "BNF-multiclass"):
            children[0].cgen()
        elif(nodeName == 'classe'):
            children[0].cgen()
        elif(nodeName == 'BNF-metodo'):
            children[0].cgen()
        elif(nodeName == 'metodo'):
            children[2].cgen()
            children[3].cgen()
        elif(nodeName == 'BNF-cmd'):
            children[0].cgen()
        elif(nodeName == "cmd"):
            children[0].cgen()
        elif(nodeName == "otherstmt"):
            if(not tokens):
                children[0].cgen()
        elif(nodeName == "condstmt"):
            children[0].cgen()
            children[1].cgen()
        elif(nodeName == "matchornot"):
            print('if_label:')
            children[0].cgen()
            if(children[1]):
                print('else_label:')
                children[1].cgen()
        elif(nodeName == 'assignment'):
            if tokens[1] == '=':
                print('\tli $a0 %s' % children[0].cgen())
            else:
                print('\tli $a0 0')
            sw('a0', 0, 'sp')
            addiu('sp','sp',-4)

        elif (nodeName == 'exp'):
            if(tokens):
                print('\tli $t1 0')
                print('\tli $t2 0')
                if(tokens[0] == '&&'):
                    print('\tand $a0 $t1 $t2')
                    addiu('\tsp','sp',-4)
                elif(tokens[0] == '||'):
                    print('\tor $a0 $t1 $t2')
                sw('a0', 0, 'sp')
                addiu('sp','sp',-4)
            else:
                return children[0].cgen()

        elif(nodeName == 'R-exp'):
            if(tokens):
                print('\tli $t1 0')
                print('\tli $t2 0')
                print('\tslt $t3 $t1 $t2')
                if(tokens[0] == '<'):
                    print('\tbeq $t3 0 lesser_than')
                    print('lesser_than:')
                elif(tokens[0] == '=='):
                    print('\tbeq $t1 $t2 equal')
                    print('equal:')
                elif(tokens[0] == '!='):
                    print('\tbne $t1 $t2 not_equal')
                    print('not_equal:')
            else:
                return children[0].cgen()
        elif(nodeName == 'A-exp'):
            if(tokens):
                print('\tli $t1 0')
                print('\tli $t2 0')
                if(tokens[0] == '+'):
                    print('\tadd $a0 $t1 $t2')
                elif(tokens[0] == '-'):
                    print('\tsub $a0 $t1 $t2')
                sw('a0', 0, 'sp')
                addiu('sp','sp',-4)
            else:
                return children[0].cgen()
        elif(nodeName == 'M-exp'):
            if(tokens):
                print('\tli $t1 0')
                print('\tli $t2 0')
                if(tokens[0] == '*'):
                    print('\tmult $a0 $t1 $t2')
                elif(tokens[0] == '/'):
                    print('\tdiv $a0 $t1 $t2')
                sw('a0', 0, 'sp')
                addiu('sp','sp',-4)
            else:
                return children[0].cgen()
        elif(nodeName == 'S-exp'):
            if(tokens):
                if(type(tokens[0]) == int):
                    return str(tokens[0])
                elif(tokens[0] == 'false'):
                    return 0
                elif(tokens[0] == 'true'):
                    return 1
                elif(tokens[0] == '-'):
                    return ('-' + tokens[1])
            else:
                return children[0].cgen()
        elif(nodeName == 'P-exp'):
            if(children):
                return children[0].cgen()
            
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