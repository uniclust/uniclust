#  UNILA parser implementation
#

from ply import *
import UNILAlex

tokens = UNILAlex.tokens

precedence = (
               ('left', 'PLUS','MINUS'),
               ('left', 'TIMES','DIVIDE'),
               ('left', 'POWER'),
               ('right','UMINUS')
)

#### Any program is a series of statements.  We represent the program as a
#### dictionary of tuples indexed by line number.

def p_program_with_starting_newlines(p):
    '''program : newline pprogram'''
    p[0] = p[2]
    
def p_program_1(p):
    '''program : pprogram'''
    p[0] = p[1]    

def p_pprogram(p):
    '''pprogram : pprogram statement SEMICOLON newline
                | statement SEMICOLON newline'''
    
    p_pprogram.line += 1
    
    #print p[2];

    if len(p) == 4 and p[1]:
       p[0] = { }
       line,stat = p[1]
       line = p_pprogram.line
       if stat[0] == 'run':
           line = 0
       p[0][line] = stat
    elif len(p) == 5:
       p[0] = p[1]
       if not p[0]: p[0] = { }
       if p[2]:
           line,stat = p[2]
           line = p_pprogram.line
           p[0][line] = stat

p_pprogram.line = 0

#### Interactive statements.

def p_statement_interactive(p):
    '''statement : RUN'''
    p[0] = (0, (p[1],0))

#### The end statement.

def p_statement_end(p):
    '''statement : END'''
    p[0] = (0, (p[1],0))

#### This catch-all rule is used for any catastrophic errors.  In this case,
#### we simply return nothing

def p_program_error(p):
    '''program : error'''
    p[0] = None
    p.parser.error = 1

#### Format of all UNILA statements. 

def p_statement(p):
    '''statement : command'''
    if isinstance(p[1],str):
        print("%s %s %s" % (p[2],"AT LINE", p[1]))
        p[0] = None
        p.parser.error = 1
    else:
        p[0] = (0,p[1])

#### Error handling for malformed statements

def p_statement_bad(p):
    '''statement : error SEMICOLON'''
    print("MALFORMED STATEMENT AT LINE %s" % p[1])
    p[0] = None
    p.parser.error = 1

#### Blank line

def p_statement_newline(p):
    '''statement : NEWLINE'''
    p[0] = None

#### Blank operator

def p_statement_blank(p):
    '''statement : SEMICOLON'''
    p[0] = None

#### shell command

def p_command_shell(p):
    '''command : SHELL expr'''
    p[0] = ('SHELL', p[2])   
    
#### connect command    
    
def p_command_connect(p):
    '''command : CONNECT expr expr expr expr'''
    p[0] = ('CONNECT', p[2], p[3], p[4], p[5])       

#### query command    
    
def p_command_query(p):
    '''command : QUERY expr'''
    p[0] = ('QUERY', p[2])       

#### PRINT statement

def p_command_print(p):
    '''command : PRINT plist'''
    p[0] = ('PRINT',p[2])

def p_command_print_bad(p):
    '''command : PRINT error'''
    p[0] = "MALFORMED PRINT STATEMENT"

#### PRINT statement with no arguments

def p_command_print_empty(p):
    '''command : PRINT'''
    p[0] = ('PRINT',[],None)

#### COMMENT statement

def p_command_rem(p):
    '''command : REM'''
    p[0] = ('REM',p[1])

#### A number. May be an integer or a float

def p_number(p):
    '''number  : INTEGER
               | FLOAT'''
    p[0] = eval(p[1])

#### A signed number.

def p_number_signed(p):
    '''number  : MINUS INTEGER
               | MINUS FLOAT'''
    p[0] = eval("-"+p[2])

#### LET statement

def p_command_let(p):
    '''command : variable EQUALS expr'''
    p[0] = ('LET',p[1],p[3])

def p_command_let_bad(p):
    '''command : variable EQUALS error'''
    p[0] = "BAD EXPRESSION IN LET"

#### Arithmetic expressions

def p_expr_binary(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | expr POWER expr'''

    p[0] = ('BINOP',p[2],p[1],p[3])

def p_expr_number(p):
    '''expr : INTEGER
            | FLOAT'''
    p[0] = ('NUM',eval(p[1]))

def p_expr_variable(p):
    '''expr : variable'''
    p[0] = ('VAR',p[1])

def p_expr_group(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = ('GROUP',p[2])

def p_expr_unary(p):
    '''expr : MINUS expr %prec UMINUS'''
    p[0] = ('UNARY','-',p[2])
    
def p_expr_string(p):
    '''expr : STRING'''
    p[0] = ('STRING',p[1])    


#### Variables

def p_variable(p):
    '''variable : ID'''
    if len(p) == 2:
       p[0] = (p[1],None,None)
    elif len(p) == 5:
       p[0] = (p[1],p[3],None)
    else:
       p[0] = (p[1],p[3],p[5])

#### List of targets for a print statement
#### Returns a list of tuples (label,expr)

def p_plist(p):
    '''plist   : plist COMMA pitem
               | pitem'''
    if len(p) > 3:
       p[0] = p[1]
       p[0].append(p[3])
    else:
       p[0] = [p[1]]

def p_item_string(p):
    '''pitem : STRING'''
    p[0] = (p[1][1:-1],None)

def p_item_string_expr(p):
    '''pitem : STRING expr'''
    p[0] = (p[1][1:-1],p[2])

def p_item_expr(p):
    '''pitem : expr'''
    p[0] = ("",p[1])
    
def p_newline(p):
    '''newline : newline NEWLINE
               | NEWLINE'''
    p[0] = None   

#### Empty
   
def p_empty(p):
    '''empty : '''

#### Catastrophic error handler
def p_error(p):
    if not p:
        print("SYNTAX ERROR AT EOF")

uparser = yacc.yacc()

def parse(data,debug=0):
    uparser.error = 0
    p = uparser.parse(data,debug=debug)
    if uparser.error: 
        return None
    return p
