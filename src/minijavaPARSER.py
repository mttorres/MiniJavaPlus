import sys
sys.path.append("../")
from src import minijavaLEX
from ply import yacc

tokens = minijavaLEX.tokens

#REGRAS DA GRAMATICA : ESCREVE-SE SEMPRE ASSIM: producao1 : producao2  TOKEN  , e utilizamos as notações EBNF
def p_prog(p):
    'prog: main {classe}'

def p_main(p):
    'main : CLASS ID '

parser = yacc.yacc()