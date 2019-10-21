import sys

sys.path.append("../")
from src import minijavaLEX
from ply import yacc

tokens = minijavaLEX.tokens


# REGRAS DA GRAMATICA : ESCREVE-SE SEMPRE ASSIM-> producao1 : producao2  TOKEN(mesmo nome definido no LEXER)  , e utilizamos as notações EBNF
# aparentemente ele so aceita BNF.. deve -se converter de EBNF para BNF
# https://stackoverflow.com/questions/2466484/converting-ebnf-to-bnf (COMO FAZER)
# note que os nomes dessas produções criadas para transformar em BNF eu dei baseado na minha da gramatica interpretação(pode estar errada)
def p_prog(p):
    # "prog : main { classe }"
    "prog : main  multiclass"


def p_multiclass(p):
    '''multiclass : multiclass classe
                  | empty '''


def p_main(p):
    "main : CLASS ID LBRACE PUBLIC STATIC VOID MAIN LPAREN STRING LBRACK RBRACK  ID RPAREN LBRACE cmd RBRACE RBRACE"


def p_classe(p):
    "classe : CLASS ID extends LBRACE variaveis metodos RBRACE"


def p_extends(p):
    '''extends : EXTENDS ID
              | empty '''


# mais especificamente variaveis opcionais de classe ou metodos
def p_variaveis(p):
    '''variaveis : variaveis var
                 | empty'''


def p_metodos(p):
    '''metodos : metodos metodo
               | empty'''


def p_var(p):
    "var : tipo ID"


def p_metodo(p):
    "metodo : PUBLIC tipo ID LPAREN paramsopcional RPAREN LBRACE variaveis cmds RETURN exp SEMI RBRACE "


def p_paramsopcional(p):
    '''paramsopcional : params
                      | empty'''


def p_cmds(p):
    '''cmds : cmds cmd
            | empty'''


def p_params(p):
    '''params : tipo ID listaparamsextra
              | empty'''


def p_listaparamsextra(p):
    '''listaparamsextra : listaparamsextra COMMA tipo ID
                        | empty'''


def p_tipo(p):
    '''tipo : INT LBRACK RBRACK
            | BOOL
            | INT
            | ID '''


def p_cmd(p):
    '''cmd : LBRACE cmds RBRACE
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
            | pexp POINT ID LPAREN expopcionalmetodo RPAREN '''


def p_expopcionalmetodo(p):
    '''expopcionalmetodo : exps
                        | empty'''


def p_exps(p):
    '''exps : exp expslist
            | empty '''


def p_expslist(p):
    '''expslist : expslist COMMA exp
                | empty '''


# define as produções vazias (fica mais facil de visualizar que escrever vazio varias vezes)
def p_empty(p):
    '''empty : '''


def p_error(p):
    print("Erro sintatico no input!")


parser = yacc.yacc(method='SLR')


def generateTree(line, SYNTAX_TREE):
    resultado = parser.parse(line)
    SYNTAX_TREE.append(resultado)
