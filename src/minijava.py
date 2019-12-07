import sys
import os
import minijavaLEX
import minijavaPARSER
from src import minijavaSEMANTIC
from utils.SYMBOL_TABLE import STable
from utils.TABLE_ENTRY import EntryProps



sys.path.insert(0, "../..")



def main():
    # print(minijavaLEX.prop)
    # print(minijavaLEX.lexer)
    # minijavaLEX.lexer.input("x = 3 + 42 * (s - t)")
    # minijavaLEX.lexer.input("class Factorial{\n\tpublic static void main(String[] a){\n\t int x;\n\tSystem.out.println(new Fac().ComputeFac(10));\n\t}\n}")
    # print(PATH)

    PATH = os.path.abspath("../resource/").replace("\\", "/")
    Files = ['Factorial.java']
    TOKEN_LIST = []
    SYNTAX_TREE = []
    outputfile = open(PATH+"/OUTPUT_MIPS_CODE.txt", 'w+')
    for i in Files:
        input = ""
        inputfile = open(PATH + "/" + i, 'r')
        for line in inputfile:
            # O parser yacc recebe O ARQUIVO COMPLETO como input, e não cada linha.
            input += line
        inputfile.close()
        minijavaPARSER.generateTree(input, SYNTAX_TREE)
        # print("=======TOKENS GERADOS=======")
        # print(TOKEN_LIST, "\n", len(TOKEN_LIST), "tokens")
        # print("============================")
        SYNTAX_TREE = list(filter(None,SYNTAX_TREE)) 
        if(len(SYNTAX_TREE) > 0):
            arvoreresposta = open("tree.txt","w+")
            print("")
            arvoreresposta.write("")
            print("======ARVORE SINTATICA %s======" % i)
            arvoreresposta.write("======ARVORE SINTATICA %s======" % i)
            arvoreresposta.write("\n")
            print(SYNTAX_TREE[0].pretty(arvoreresposta), "\n")
            arvoreresposta.write("\n")
            #print("============================")
            arvoreresposta.close()

            # declara o escopo global(TABELA PRINCIPAL):
            escopoglobal = STable()
            TABLE_POINTER = []
            TABLE_POINTER.append(escopoglobal)
            minijavaSEMANTIC.processTree(SYNTAX_TREE[0],TABLE_POINTER[0])
            #print(TABLE_POINTER[0])


            #gera código
            SYNTAX_TREE[0].cgen(TABLE_POINTER[0],outputfile)


if __name__ == '__main__':
    main()
