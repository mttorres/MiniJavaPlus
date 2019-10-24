import sys
import os
import minijavaLEX
import minijavaPARSER

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
        if(len(list(filter(None,SYNTAX_TREE))) > 0):
            arvoreresposta = open("tree.txt","w+")
            print("")
            arvoreresposta.write("")
            print("======ARVORE SINTATICA %s======" % i)
            arvoreresposta.write("======ARVORE SINTATICA %s======" % i)
            arvoreresposta.write("\n")
            print(SYNTAX_TREE[0].pretty(arvoreresposta), "\n")
            arvoreresposta.write("\n")
            print("============================")
            arvoreresposta.close()


if __name__ == '__main__':
    main()
