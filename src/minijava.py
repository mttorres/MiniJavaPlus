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

	for i in Files:
		inputfile = open(PATH+"/"+i, 'r')
		for line in inputfile:
			minijavaLEX.lexer.input(line)
			while True:
				token = minijavaLEX.lexer.token()
				if not token:
					break
				print(token) # um objeto token tem os seguintes atributos: TIPO, VALOR(lexema), LINHA, POS
				TOKEN_LIST.append(token)
		inputfile.close()


if __name__ == '__main__':
	main()
	