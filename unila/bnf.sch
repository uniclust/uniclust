    <program> ::= <newline> <pprogram> | <pprogram> | <error>
    <pprogram> ::= <pprogram> <statement> SEMICOLON <newline>
                | <statement> SEMICOLON <newline>
    <statement> ::= RUN | END |  <command> | <error> SEMICOLON | NEWLINE | SEMICOLON
    <command> ::= SHELL <expr> | CONNECT <expr> <expr> <expr> <expr> | QUERY <expr>
		| PRINT <plist> | PRINT <error> |  PRINT | REM
    <number>  ::= INTEGER
                | FLOAT
	        | MINUS INTEGER
                | MINUS FLOAT
    <command> ::= <variable> EQUALS <expr> | <variable> EQUALS <error>
    <expr> ::= <expr> PLUS <expr>  | <expr> POWER <expr> | INTEGER | FLOAT | <variable>
		| LPAREN <expr> RPAREN | MINUS <expr> %<prec> UMINUS | STRING
    <variable> ::= ID
    <plist>   ::= <plist> COMMA <pitem>
                | <pitem>
    <pitem> ::= STRING | STRING <expr> | <expr>
    <newline> ::= <newline> NEWLINE
                | NEWLINE
    <empty> ::= 
