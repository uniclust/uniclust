# An implementation of UNILA - option representation languge of arbitrary program

from ply import *

keywords = {
    'read' :    'READ',
    'data' :    'DATA',
    'goto' :    'GOTO',
    'if' :      'IF',
    'then' :    'THEN',
    'for' :     'FOR',
    'to' :      'TO', 
    'find' :    'FIND',
    'table' :   'TABLE',
    'def' :     'DEF', 
    'return' :  'RETURN',
    'UTable' :  'UTABLE', 
    'UThread' : 'UTHREAD', 
    'UFrame' :  'UFRAME',
    'run' :     'RUN', 
    'print' :   'PRINT', 
    'shell' :   'SHELL',
    'end' :     'END',
    'connect' : 'CONNECT',
    'query' :   'QUERY'
}

tokens = list(keywords.values()) + [
     'EQUALS','PLUS','MINUS','TIMES','DIVIDE','POWER', # Mathematical operations
     'LPAREN','RPAREN','LT','LE','GT','GE','NE',       # Comparison operators
     'SEMICOLON', 'COMMA', 'LATTICESIGN',	         		# Punctuation marks
     'ID','NEWLINE', 'REM',					# Supporting characters		
     'INTEGER', 'FLOAT', 'STRING'
]

t_ignore = ' \t'

def t_REM(t):
    r'comment .*'
    return t

def t_ID(t):
    r'[A-Za-z][A-Za-z0-9]*'
    t.type = keywords.get(t.value, 'ID')
    return t
    
t_EQUALS  = r'='
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_POWER   = r'\^'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LT      = r'<'
t_LE      = r'<='
t_GT      = r'>'
t_GE      = r'>='
t_NE      = r'<>'
t_COMMA   = r'\,'
t_SEMICOLON   = r';'
#t_COMMENT = r'#'
t_INTEGER = r'\d+'    
t_FLOAT   = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
# t_Double =
t_STRING = r'\".*?\"'
#t_UTable =
#t_UThread = 
#t_UFrame =
#t_ID =


def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t

def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

lex.lex(debug=0)

