 """
Lexer and Parser rules
"""


def merge(l1, l2):
    if l1 is None:
        return l2
    if l2 is None:
        return l1
    ret = []
    for i1 in l1:
        for i2 in l2:
            ret.append(i1+i2)
    return ret 

paths = []

# List of token names.   This is always required
tokens = (
     'WORD',
     'OPTION',
     'OR',
     'LBR',
     'RBR',
     'EOL',
     'LSB',
     'RSB'
)
 
# Regular expression rules for simple tokens
t_OR    = r'\|'
t_LBR   = r'\('
t_RBR   = r'\)'
t_LSB   = r'\['
t_RSB   = r'\]'

def t_WORD(t):
    r'[a-zA-Z]+'
    t.value = [[t.value]]
    return t

def t_OPTION(t):
    r'-[a-zA-Z]{1}(\s+\<.+?\>)?'
    t.value = [[t.value]]
    return t   
 
# A regular expression rule with some action code
# Define a rule so we can track line numbers
def t_EOL(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t
 
# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
 
# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
 
# Build the lexer
# lexer = lex.lex()

def p_all(p):
    '''all : 
           | all line'''
    pass

def p_line(p):
    ''' line : path EOL
    '''
    if len(p) > 1:
        for pt in p[1]:
            paths.append(pt)
    pass
 
def p_path(p):
    ''' path : wrdopt
             | path wrdopt
             | path collection
             | path alternatives
     '''
    if len(p) < 2:
        p[0] = list()
    elif len(p) < 3:
        p[0] = p[1]
    else:
        p[0] = merge(p[1],p[2])
    # paths.append(p[0])
    
    
def p_group(p):
    ''' group : LBR alternatives RBR
              | LBR path RBR    
    '''
    p[0] = p[2]

def p_optional_group(p):
    ''' ogroup : LSB alternatives RSB
               | LSB path RSB    
    '''
    p[0] = p[2] + [[]]

def p_alternatives(p):
    ''' alternatives : alternatives OR wrdopt
                     | alternatives OR collection
                     | wrdopt OR collection
                     | collection OR wrdopt
                     | wrdopt OR wrdopt
                     '''
    p[0] = p[1] + p[3]
           
def p_word_or_option(p):
    ''' wrdopt : WORD 
               | OPTION
    '''
    p[0] = p[1]

def p_collection(p):
    ''' collection : group 
                   | ogroup
    '''
    p[0] = p[1]