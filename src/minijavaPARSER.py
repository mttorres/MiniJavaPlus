import sys
sys.path.append("../")
from src import minijavaLEX
from ply import yacc

tokens = minijavaLEX.tokens

#REGRAS DA GRAMATICA : ESCREVE-SE SEMPRE ASSIM-> producao1 : producao2  TOKEN(mesmo nome definido no LEXER)  , e utilizamos as notações EBNF
# aparentemente ele so aceita BNF.. deve -se converter de EBNF para BNF
def p_prog(p):
    "prog : main { classe }"

def p_main(p):
    "main : CLASS ID LBRACE PUBLIC STATIC VOID MAIN LPAREN STRING LBRACK RBRACK RPAREN LBRACE cmd RBRACE RBRACE"

def p_classe(p):
    "classe : CLASS ID [EXTENDS ID] LBRACE {var} {metodo} RBRACE"

def p_var(p):
    "var : tipo ID"

def p_metodo(p):
    "metodo : PUBLIC tipo ID LPAREN [params] RPAREN LBRACE {var} {cmd} RETURN exp SEMI RBRACE "

def p_params(p):
    "params : tipo ID {COMMA tipo ID}"

def p_tipo(p):
    '''tipo : INT LBRACK RBRACK
            | BOOL
            | INT
            | ID '''

def p_cmd(p):
   '''cmd : LBRACE {cmd} RBRACE
          | IF LPAREN exp RPAREN cmd
          | IF LPAREN exp RPAREN cmd ELSE cmd
          | WHILE LPAREN exp RPAREN cmd
          | SOUTPL LPAREN exp RPAREN SEMI
          | ID ASSIGN exp SEMI
          | ID LBRACK exp RBRACK ASSIGN exp SEMI '''

def p_exp(p):
    '''exp : exp LAND rexp
           | exp LOR rexp
           | rexp '''

def p_rexp(p):
    '''rexp : rexp LT aexp
            | rexp EQ aexp
            | rexp NE aexp
            | aexp'''

def p_aexp(p):
    '''aexp : aexp PLUS mexp
            | aexp MINUS mexp
            | mexp'''

def p_mexp(p):
    '''mexp : mexp TIMES sexp
            | mexp DIVIDE sexp
            | sexp'''

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

def p_pexp(p):
    '''pexp : ID
            | THIS
            | NEW ID LPAREN RPAREN
            | pexp POINT ID
            | pexp POINT ID LPAREN [exps] RPAREN '''

def p_exps(p):
    '''exps : exp {COMMA exp}'''

def p_error(p):
    print("Erro sintatico no input!")

parser = yacc.yacc()

def generateTree(line,SYNTAX_TREE):
    resultado = parser.parse(line)
    SYNTAX_TREE.append(resultado)