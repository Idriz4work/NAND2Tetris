import re

class AnalyserTable:
    keywords = {
        "class": "<class>",
        "constructor": "<constructor>",
        "function": "<function>",
        "method": "<method>",
        "field": "<field>",
        "static": "<static>",
        "var": "<var>",
        "int": "<int>",
        "char": "<char>",
        "boolean": "<boolean>",
        "void": "<void>",
        "true": "<true>",
        "false": "<false>",
        "null": "<null>",
        "this": "<this>",
        "let": "<let>",
        "do": "<doStatement>",
        "if": "<ifStatement>",
        "else": "<elseStatement>",
        "while": "<whileStatement>",
        "return": "<returnStatement>"
    }
    def some_method(self):
        # Now class_token will be "<class>"
        class_token = self.keywords["class"]
        return class_token
    
    def get_char(self, code):
        for char, sy in self.codes.items():
            if code == sy:
                return char
        return "Not found"

    def __init__(self):
        # Token Symbols
        self.LBRACE = "{"
        self.RBRACE = "}"
        self.LPAREN = "("
        self.RPAREN = ")"
        self.LSQUARE = "["
        self.RSQUARE = "]"
        self.DOT = "."
        self.COMMA = ","
        self.SEMICOLON = ";"
        self.PLUS = "+"
        self.MINUS = "-"
        self.STAR = "*"
        self.SLASH = "/"
        self.AND = "&"
        self.PIPE = "|"
        self.LT = "<"
        self.GT = ">"
        self.EQUAL = "="
        self.TILDE = "~"

        # All Symbols
        self.allSymbols = {
            self.LBRACE, self.RBRACE, self.LPAREN, self.RPAREN, self.LSQUARE, self.RSQUARE,
            self.DOT, self.COMMA, self.SEMICOLON, self.PLUS, self.MINUS, self.STAR,
            self.SLASH, self.AND, self.PIPE, self.LT, self.GT, self.EQUAL, self.TILDE
        }

        # Operators
        self.Operators = {
            self.PLUS, self.MINUS, self.STAR, self.SLASH, self.AND, self.PIPE,
            self.LT, self.GT, self.EQUAL
        }

        # XML Symbols
        self.XmlSymbols = {
            self.LBRACE: self.LBRACE,
            self.RBRACE: self.RBRACE,
            self.LPAREN: self.LPAREN,
            self.RPAREN: self.RPAREN,
            self.LSQUARE: self.LSQUARE,
            self.RSQUARE: self.RSQUARE,
            self.DOT: self.DOT,
            self.COMMA: self.COMMA,
            self.SEMICOLON: self.SEMICOLON,
            self.PLUS: self.PLUS,
            self.MINUS: self.MINUS,
            self.STAR: self.STAR,
            self.SLASH: self.SLASH,
            self.AND: "&amp;",
            self.PIPE: self.PIPE,
            self.LT: "&lt;",
            self.GT: "&gt;",
            self.EQUAL: self.EQUAL,
            self.TILDE: self.TILDE,
        }

# Example usage
analyser_table = AnalyserTable()
