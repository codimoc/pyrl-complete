import ply.lex as lex
import ply.yacc as yacc
from pyrl.parser import clear,paths, rules

# Test it out
data = '''test zero
          get zero (one | (two | three) )
          set (one | two) | zero
          get -h | (-d <domain> -a <access> )
          test [first | second]
       '''

# build the lexer
lexer = lex.lex(module=rules)


# Give the lexer some input
lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)


# Build the parser
parser = yacc.yacc(module=rules)

clear() # clear all paths before parsing
res = parser.parse(data)
print(paths())