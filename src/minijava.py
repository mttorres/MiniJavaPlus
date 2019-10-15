import sys

from src import minijavaLEX

sys.path.insert(0, "../..")


def main():
	print(minijavaLEX.prop)
	print(minijavaLEX.lexer)
	minijavaLEX.lexer.input("x = 3 + 42 * (s - t)")
	while True:
		token = minijavaLEX.lexer.token()
		if not token:
			break
		print(token)

if __name__ == '__main__':
	main()
	