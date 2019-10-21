import sys
sys.path.append("../")
from ply import lex

prop = True

# Lista dos nomes dos tokens.

# palavras reservadas: System.out.println e outras

reserved = {
    'boolean': 'BOOL',
    'class'  : 'CLASS',
    'extends': 'EXTENDS' ,
    'public' : 'PUBLIC',
    'static' : 'STATIC',
    'void'   : 'VOID',
    'main'	 : 'MAIN',
    'String' : 'STRING',
    'return' : 'RETURN',
    'int'    : 'INT',
    'if'     : 'IF',
    'else'   : 'ELSE',
    'while'  : 'WHILE',
    'length' : 'LENGTH',
    'true'   : 'TRUE',
    'false'  : 'FALSE',
    'this'   : 'THIS',
    'new'    : 'NEW',
    'null'   : 'NULL',
    'System.out.println': 'SOUTPL'
}


tokens =  tuple(reserved.values()) + (
    
	##operações em expressoes (+,-,*,/, ||, &&, !, <, <=, >, >=, ==, !=)
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',  # ". Isso facilita o restante do compilador. Também não há um operador de divisão." , MAS NA BNF TEM !
    'LOR',
    'LAND',
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE','LNOT',

    # delimitadores ( ) [ ] { } , . ; :
    'LPAREN', 'RPAREN',
    'LBRACK', 'RBRACK',
    'LBRACE', 'RBRACE',
    'COMMA', 'POINT', 'SEMI', 'COLON',

    #atribuição (id, =,  )

    'ASSIGN','ID'


)


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
t_COMMA = r','
t_POINT = r'\.'
t_SEMI = r';'
t_COLON = r':'


# para todas as demais er's além das regras simples (ajuda a otimização)
def t_ID(t):
    r'System.out.println|[A-Za-z_][\w]*'   # print | qualquermenosnumero + qualquer*
    t.type = reserved.get(t.value, 'ID') # verifica as palavras reservadas
    return t

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# basicamente ele nao faz nada só reconhece o \n e "pula a linha" na classe lexer (que possui diversos atributos um dele é lineno (linenumber))
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# comentarios de zero ou mais linhas (BARRA ESTRELA)
def t_COMMENT_STAR(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

#NOTE QUE a ordem das funções é importante na ordenação de qual vai dar match primeiro! usar o comment // antes pode fazer ele nunca dar match no barra estrela
def t_COMMENT(t):
    r'//.*'
    pass


# ignorar tab's 
t_ignore_TAB = r'\t'
t_ignore_FF = r'\f'
t_ignore_CAR = r'\r'
t_ignore_SPACE = r'\s'
    
# reporta erros
def t_error(t):
    print("Caracter ilegal em: '%s'" % t.value[0])
    t.lexer.skip(1) # pula o char e joga a primeira ocorrencia de erro

lexer = lex.lex()

def generateTokens(line,TOKEN_LIST):
    lexer.input(line)
    while True:
        token = lexer.token()
        if not token:
            break
        #print(token)  # um objeto token tem os seguintes atributos: TIPO, VALOR(lexema), LINHA, POS
        TOKEN_LIST.append(token)