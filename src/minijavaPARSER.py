import sys
sys.path.append("../")
from ply import yacc
from src import minijavaLEX
from utils.tree import Node

# REGRAS DA GRAMATICA : ESCREVE-SE SEMPRE ASSIM-> producao1 : producao2  TOKEN(mesmo nome definido no LEXER), 
# e utilizamos as notações EBNF, aparentemente ele so aceita BNF. Deve -se converter de EBNF para BNF
# https://stackoverflow.com/questions/2466484/converting-ebnf-to-bnf (COMO FAZER)
# note que os nomes dessas produções criadas para transformar em BNF
# eu dei baseado na minha interpretação da gramatica (pode estar errada)
def p_prog(p):
    "prog : CLASS ID extends LBRACE PUBLIC main RBRACE multiclass"
    p[0] = Node("prog", [p[3], p[6], p[8]], [p[1], p[2], p[4], p[5], p[7]])

def p_multiclass(p):
    '''multiclass : multiclass classe
                   |'''
    if len(p) > 2:
        p[0] = Node("BNF-multiclass", [p[1], p[2]])

def p_main(p):
    "main :  STATIC VOID MAIN LPAREN STRING LBRACK RBRACK ID RPAREN LBRACE cmds RBRACE"
    tokens = [p[1],p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[12]]
    p[0] = Node("main", [p[11]], tokens)

def p_classe(p):
    '''classe : CLASS ID extends LBRACE variaveis metodos RBRACE '''
    tokens = [p[1], p[2], p[4], p[7]]
    p[0] = Node("classe", [p[3], p[5], p[6]], tokens)

def p_extends(p):
    '''extends : EXTENDS ID
    		   |'''
    if len(p) > 2:
        tokens = [p[2],p[1]]
        p[0] = Node("BNF-extends", leaf=tokens)

# mais especificamente variaveis opcionais de classe ou metodos
def p_variaveis(p):
    '''variaveis : variaveis var
                  |'''
    if len(p) > 2:
        p[0] = Node("BNF-variaveis", [p[1], p[2]])

def p_metodos(p):
    '''metodos : metodos metodo
               | '''
    if len(p) > 2:
        p[0] = Node("BNF-metodo", [p[1], p[2]])

def p_var(p):
    "var : tipo ID SEMI"
    tokens = [p[2],p[3]]
    p[0] = Node("var", [p[1]], tokens)

def p_metodo(p):
    "metodo : PUBLIC tipo ID LPAREN paramsopcional RPAREN LBRACE variaveis cmds RETURN exp SEMI RBRACE "
    tokens = [p[1], p[3], p[4], p[6], p[7], p[10], p[12], p[13]]
    p[0] = Node("metodo", [p[2], p[5], p[8], p[9], p[11]], tokens)

def p_paramsopcional(p):
    '''paramsopcional : params
                      | '''
    p[0] = Node("BNF-params", [p[1]])

def p_cmds(p):
    '''cmds : cmds cmd
            | cmd'''
    if len(p) > 2:
        p[0] = Node("BNF-cmd", [p[1], p[2]])
    else:
        p[0] = Node("BNF-cmd", [p[1]])

def p_params(p):
    '''params : tipo ID listaparamsextra'''
    tokens = [p[2]]
    p[0] = Node("params", [p[1], p[3]], tokens)

def p_listaparamsextra(p):
    '''listaparamsextra : listaparamsextra COMMA tipo ID
                        | '''
    if len(p) > 2:
        tokens = [p[2], p[4]]
        p[0] = Node("BNF-paramsExtra", [p[1], p[3]], tokens)

def p_tipo(p):
    '''tipo : INT LBRACK RBRACK
            | BOOL
            | INT
            | ID '''
    if( len(p) > 2):
        tokens = [p[1],p[2],p[3]]
        p[0] = Node("tipo", leaf=tokens)
    else:
        p[0] = Node("tipo", leaf=[p[1]])

def p_cmd(p):
    '''cmd :  condstmt
          |   otherstmt'''
    non_terms = [p[1]]
    tokens = []
    p[0] = Node("cmd", non_terms, tokens)


def p_otherstmt(p):
    '''otherstmt : LBRACE cmds RBRACE
          | LBRACE RBRACE
          | WHILE LPAREN exp RPAREN cmd
          | SOUTPL LPAREN exp RPAREN SEMI
          | ID ASSIGN exp SEMI
          | ID LBRACK exp RBRACK ASSIGN exp SEMI '''
    non_terms = []
    tokens = []
    if(p[1] != '{'):
        non_terms.append(p[3])
        if(p[2] == '['):
            non_terms.append(p[6])
            tokens.extend([p[1],p[2],p[4],p[5],p[7]])
        elif(p[1] == 'while'):
            non_terms.append(p[5])
            tokens.extend([p[1],p[2],p[4]])
        elif(p[2] == '='):
            tokens.extend([p[1],p[2],p[4]])
        else:
            tokens.extend([p[1],p[2],p[4],p[5]])
    elif(p[1] == '{'):
        if (len(p) > 2) :
            non_terms.append(p[2])
            tokens.extend([p[1],p[3]])
        else:
            tokens.extend([p[1],p[2]])

    p[0] = Node("otherstmt", non_terms, tokens)


def p_condstmt(p):
    '''condstmt : IF LPAREN exp RPAREN cmd matchornot'''
    p[0] = Node("condstmt",[p[3], p[5], p[6]], [p[1], p[2], p[4]])



def p_matchornot(p):
    '''matchornot : ELSE cmd
             |  '''
    p[0] = Node("matchornot", [p[2]], [p[1]])

def p_exp(p):
    '''exp : exp LAND rexp
           | exp LOR rexp
           | rexp '''
    if len(p) > 2:
        p[0] = Node("exp", [p[1], p[3]], [p[2]])
    else:
        p[0] = Node("exp", [p[1]])

def p_rexp(p):
    '''rexp : rexp LT aexp
            | rexp EQ aexp
            | rexp NE aexp
            | aexp'''
    if len(p) > 2:
        p[0] = Node("R-exp", [p[1], p[3]], [p[2]])
    else:
        p[0] = Node("R-exp", [p[1]])

def p_aexp(p):
    '''aexp : aexp PLUS mexp
            | aexp MINUS mexp
            | mexp'''
    if len(p) > 2:
        p[0] = Node("A-exp", [p[1], p[3]], [p[2]])
    else:
        p[0] = Node("A-exp", [p[1]])

def p_mexp(p):
    '''mexp : mexp TIMES sexp
            | mexp DIVIDE sexp
            | sexp'''
    if len(p) > 2:
        p[0] = Node("M-exp", [p[1], p[3]], [p[2]])
    else:
        p[0] = Node("M-exp", [p[1]])

def p_sexp(p):  # MINUS sexp  ?
    '''sexp : LNOT sexp
            | MINUS sexp
            | TRUE
            | FALSE
            | NUMBER
            | NULL
            | NEW INT LBRACK exp RBRACK
            | pexp POINT LENGTH
            | pexp LBRACK exp RBRACK
            | pexp '''
    tokens = []
    non_terms = []
    if type(p[1]) != Node:
        tokens.append(p[1])
        if p[1] == '!' or p[1]== '-':
            non_terms.append(p[2])
        if p[1] == 'new':
            non_terms.append(p[4])
            tokens.extend([p[2],p[3],p[5]])
    else:
        non_terms.append(p[1])
        if len(p) == 4:
            tokens.extend([p[2],p[3]])
        elif len(p) == 5:
            non_terms.append(p[3])
            tokens.extend([p[2],p[4]])
    p[0] = Node("S-exp", non_terms, tokens)
    
    

def p_pexp(p):
    '''pexp : ID
            | THIS 
            | NEW ID LPAREN RPAREN
            | LPAREN exp RPAREN
            | pexp POINT ID LPAREN expopcionalmetodo RPAREN
            | pexp POINT ID LPAREN RPAREN 
            | pexp POINT ID'''
    non_terms = []
    tokens = []
    if(type(p[1]) != Node):
        tokens.append(p[1])
        if len(p) == 5:
            tokens.extend([p[2],p[3],p[4]])
        elif len(p) == 4:
            tokens.append(p[3])
            non_terms.append(p[2])
    else:
        non_terms.append(p[1])
        tokens.extend([p[2],p[3]])
        if(len(p) > 4):
            if p[5] == ')':
                tokens.extend([p[4],p[5]])
            else:
                non_terms.append(p[5])
                tokens.extend([p[4],p[6]])
    p[0] = Node("P-exp", non_terms, tokens)

def p_expopcionalmetodo(p):
    '''expopcionalmetodo : exps '''
    
    p[0] = Node("BNF-expOpcional", [p[1]])

def p_exps(p):
    '''exps : exp expslist'''
    if len(p) > 2:
        p[0] = Node("BNF-exps", [p[1], p[2]])

def p_expslist(p):
    '''expslist : expslist COMMA exp
                |  '''
    if len(p) > 2:
        p[0] = Node("BNF-expList", [p[1], p[3]],[p[2]])

def p_error(p):
    if p:
        tok = parser.token()
        print("Erro de sintaxe: '%s'        . . . . antes do token '%s' na linha %d coluna %d"  % (p.value, tok.value, p.lineno, p.lexpos))
        return tok 
    else:
        print("Erro de sintaxe - EOF")

precedence = (
     ('nonassoc', 'LT', 'GT', 'LE', 'GE', 'EQ', 'NE'),  # Nonassociative operators
     ('left', 'PLUS', 'MINUS'),
)

# Setup and initialization
tokens = minijavaLEX.tokens
parser = yacc.yacc(method='SLR')

# Parses input file and pushes every AST Node to a array. 
def generateTree(input, SYNTAX_TREE):
    resultado = parser.parse(input)
    SYNTAX_TREE.append(resultado)
