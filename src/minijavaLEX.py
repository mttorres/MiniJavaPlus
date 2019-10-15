
import sys
sys.path.insert(0, "../..")
from ply import lex

prop = True

# Lista dos nomes dos tokens.

# palavras reservadas:

reserved = (
    'boolean', 'class', 'extends', 'public', 'static', 'void', 'main', 'String',
    'return', 'int', 'if', 'else', 'while', 'System.out.println', 'length', 'true', 'false', 'this',
    'new', 'null'
)


##### remover depois############
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'


# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
##### remover depois############

lexer = lex.lex()


