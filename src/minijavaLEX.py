
import sys
sys.path.insert(0, "../..")
from ply import lex

prop = True

# Lista dos nomes dos tokens.

# palavras reservadas: System.out.println e outras

reserved = {
    'BOOL'    : 'boolean' , 
    'CLASS'   : 'class', 
    'EXTENDS' : 'extends' , 
    'PUBLIC' : 'public', 
    'STATIC' : 'static', 
    'VOID'   : 'void',
    'MAIN'	 : 'main',  
    'STRING' : 'String',
    'RETURN' : 'return', 
    'INT'   : 'int',
    'IF'     : 'if', 
    'ELSE'   : 'else', 
    'WHILE'  : 'while', 
    'SOUTPL' : 'System.out.println',
    'LENGTH' : 'length',
    'TRUE'   : 'true',
    'FALSE'  : 'false', 
    'THIS'   : 'this',
    'NEW'    : 'new', 
    'NULL'   : 'null'
}


tokens =  tuple(reserved) + (
    
	##operações em expressoes (+,-,*,/, ||, &&, !, <, <=, >, >=, ==, !=)
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',  ## ". Isso facilita o restante do compilador. Também não há um operador de divisão." , MAS NA BNF TEM !
    'LOR',
    'LAND',
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',

    # delimitadores ( ) [ ] { } , . ; :
    'LPAREN', 'RPAREN',
    'LBRACK', 'RBRACK',
    'LBRACE', 'RBRACE',
    'COMMA', 'POINT', 'SEMI', 'COLON',

    #atribuição (id, =,  )

    'ASSING'


)


def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved.get(t.value, "ID") # verifica as palavras reservadas
    return t


# Regular expression rules for simple tokens
t_PLUS = r'\+'   # nota: caracteres que sao usados em em ER'S devem ser escapados com \
t_MINUS = r'-'
t_TIMES = r'\*'  
t_DIVIDE = r'/'   # por enquanto deixar aqui (na BNF tem divisão)
t_LOR = r'\|\|'
t_LAND = r'&&'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_LNOT = r'!'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACK = r'\['
t_RBRACK = r'\]'





# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# basicamente ele nao faz nada só reconhece o \n e "pula a linha" na classe lexer (que possui diversos atributos um dele é lineno (linenumber))
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# ignorar tab's 
t_ignore = ' \t'


# reporta erros
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1) # pula o char e joga a primeira ocorrencia de erro


lexer = lex.lex()


