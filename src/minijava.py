import sys
import os
from src import minijavaLEX

sys.path.insert(0, "../..")


def main():
	#print(minijavaLEX.prop)
	#print(minijavaLEX.lexer)
	#minijavaLEX.lexer.input("x = 3 + 42 * (s - t)")
	#minijavaLEX.lexer.input("class Factorial{\n\tpublic static void main(String[] a){\n\t int x;\n\tSystem.out.println(new Fac().ComputeFac(10));\n\t}\n}")
	#print(PATH)

	PATH = os.path.abspath("../resource/").replace("\\","/")
	Files = ['Factorial.java','Fac.java']
	TOKEN_LIST = []
	SYNTAX_TREE = []

	for i in Files:
		inputfile = open(PATH+"/"+i, 'r')
		for line in inputfile:
			minijavaLEX.generateTokens(line,TOKEN_LIST)
		inputfile.close()
	print(len(TOKEN_LIST))
	print(TOKEN_LIST)


if __name__ == "__main__" and __package__ is None:
	from sys import path
	from os.path import dirname as dir
	main()