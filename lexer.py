import ply.lex as lex
from ply.lex import TOKEN


class Lexer(object):
    tokens = ('NUMBER', 'ID', 'BOOL_VAL')
    literals = ('+', '-', '*', '/', '(', ')', '>', '<', '=')
    t_ignore = "\n|\r|\t|' '"
    reserved = {
        'and': 'AND', 'or': 'OR', 'not': 'NOT',
        'mod': 'MODULES', 'if': 'IF', 'define': 'DEFINE', 'fun': 'FUN',
        'print-num': 'PRINT_NUM', 'print-bool': 'PRINT_BOOL',
    }
    digit = r'[0-9]'
    letter = r'[a-z]'
    tokens = tokens + tuple(reserved.values())

    @TOKEN(fr'0| [1-9]{digit}* | \-[1-9]{digit}*')
    def t_NUMBER(self, t):
        t.value = int(t.value)
        return t

    @TOKEN(fr'{letter}({letter}|{digit}|\-)*')
    def t_ID(self, t):
        t.type = Lexer.reserved.get(t.value, 'ID')  # Check for reserved words
        return t

    def t_BOOL_VAL(self, t):
        r'[#]t | [#]f'
        if t.value == "#t":
            t.value = True
        if t.value == "#f":
            t.value = False
        return t

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def build(self, **kwargs):
        Lexer.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        Lexer.lexer.input(data)
        for i in Lexer.lexer:
            print(i)


