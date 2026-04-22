"""
Recursive-Descent Predictive Parser for Mini-JavaScript Grammar
Group 19 - Compiler Construction
"""

import sys
from lexer import lex

# ─────────────────────────────────────────────────────────────
# PARSE TREE NODE
# ─────────────────────────────────────────────────────────────
class Node:
    def __init__(self, label, children=None, token=None):
        self.label    = label
        self.children = children or []
        self.token    = token          # set for leaf nodes

    def is_leaf(self):
        return self.token is not None

    def pretty(self, indent=0, last=True, prefix=""):
        connector = "└── " if last else "├── "
        if indent == 0:
            line = self.label
        else:
            line = prefix + connector + self.label
        if self.token:
            line += f'  [{self.token[0]}: {self.token[1]!r}]'
        print(line)
        new_prefix = prefix + ("    " if last else "│   ")
        for i, child in enumerate(self.children):
            child.pretty(indent + 1, i == len(self.children) - 1, new_prefix)

# ─────────────────────────────────────────────────────────────
# PARSER
# ─────────────────────────────────────────────────────────────
class Parser:
    def __init__(self, tokens):
        self.tokens  = tokens
        self.pos     = 0
        self.errors  = []

    def peek(self):
        return self.tokens[self.pos]

    def consume(self, tok_type=None, lexeme=None):
        tok = self.tokens[self.pos]
        if tok_type and tok[0] != tok_type:
            self.error(f"Expected token type '{tok_type}' but got '{tok[0]}' ({tok[1]!r})")
            return ('ERR', tok[1])
        if lexeme and tok[1] != lexeme:
            self.error(f"Expected '{lexeme}' but got {tok[1]!r}")
            return ('ERR', tok[1])
        self.pos += 1
        return tok

    def error(self, msg):
        tok = self.peek()
        full = f"[Syntax Error] {msg}  (near '{tok[1]}')"
        self.errors.append(full)
        print(full)

    def match_kw(self, word):
        tok = self.peek()
        return tok[0] == 'KW' and tok[1] == word

    def match_op(self, ch):
        tok = self.peek()
        return tok[0] == 'OP' and tok[1] == ch

    # ── grammar rules ─────────────────────────────────────────

    def parse_program(self):
        node = Node("program")
        node.children.append(self.parse_stmt_list())
        return node

    def parse_stmt_list(self):
        node = Node("stmt_list")
        while True:
            tok = self.peek()
            if tok[0] in ('KW', 'ID') or (tok[0] == 'EOF'):
                if tok[0] == 'EOF' or tok[1] == '}':
                    break
                node.children.append(self.parse_stmt())
            else:
                break
        return node

    def parse_stmt(self):
        tok = self.peek()
        node = Node("stmt")
        if self.match_kw('let'):
            node.children.append(self.parse_let_stmt())
        elif self.match_kw('if'):
            node.children.append(self.parse_if_stmt())
        elif self.match_kw('while'):
            node.children.append(self.parse_while_stmt())
        elif tok[0] == 'ID':
            node.children.append(self.parse_assign_stmt())
        else:
            self.error(f"Unexpected token '{tok[1]}'; expected statement")
            self.pos += 1 
        return node

    def parse_let_stmt(self):
        node = Node("let_stmt")
        t = self.consume('KW', 'let');   node.children.append(Node(f"'let'", token=t))
        t = self.consume('ID');          node.children.append(Node(f"ID", token=t))
        t = self.consume('OP', '=');     node.children.append(Node(f"'='", token=t))
        node.children.append(self.parse_expr())
        t = self.consume('OP', ';');     node.children.append(Node(f"';'", token=t))
        return node

    def parse_assign_stmt(self):
        node = Node("assign_stmt")
        t = self.consume('ID');          node.children.append(Node("ID", token=t))
        t = self.consume('OP', '=');     node.children.append(Node("'='", token=t))
        node.children.append(self.parse_expr())
        t = self.consume('OP', ';');     node.children.append(Node("';'", token=t))
        return node

    def parse_if_stmt(self):
        node = Node("if_stmt")
        t = self.consume('KW', 'if');    node.children.append(Node("'if'", token=t))
        t = self.consume('OP', '(');     node.children.append(Node("'('", token=t))
        node.children.append(self.parse_cond())
        t = self.consume('OP', ')');     node.children.append(Node("')'", token=t))
        t = self.consume('OP', '{');     node.children.append(Node("'{'", token=t))
        node.children.append(self.parse_stmt_list())
        t = self.consume('OP', '}');     node.children.append(Node("'}'", token=t))
        return node

    def parse_while_stmt(self):
        node = Node("while_stmt")
        t = self.consume('KW', 'while'); node.children.append(Node("'while'", token=t))
        t = self.consume('OP', '(');     node.children.append(Node("'('", token=t))
        node.children.append(self.parse_cond())
        t = self.consume('OP', ')');     node.children.append(Node("')'", token=t))
        t = self.consume('OP', '{');     node.children.append(Node("'{'", token=t))
        node.children.append(self.parse_stmt_list())
        t = self.consume('OP', '}');     node.children.append(Node("'}'", token=t))
        return node

    def parse_cond(self):
        node = Node("cond")
        node.children.append(self.parse_expr())
        t = self.consume('OP', '<');     node.children.append(Node("'<'", token=t))
        node.children.append(self.parse_expr())
        return node

    def parse_expr(self):
        node = Node("expr")
        node.children.append(self.parse_term())
        node.children.append(self.parse_expr_tail())
        return node

    def parse_expr_tail(self):
        node = Node("expr_tail")
        if self.match_op('+'):
            t = self.consume('OP', '+'); node.children.append(Node("'+'", token=t))
            node.children.append(self.parse_term())
            node.children.append(self.parse_expr_tail())
        else:
            node.children.append(Node("ε"))
        return node

    def parse_term(self):
        node = Node("term")
        tok = self.peek()
        if tok[0] == 'NUM':
            t = self.consume('NUM');     node.children.append(Node("NUM", token=t))
        elif tok[0] == 'ID':
            t = self.consume('ID');      node.children.append(Node("ID", token=t))
        else:
            self.error(f"Expected NUM or ID in expression, got '{tok[1]}'")
        return node

# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else 'sample.js'
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        sys.exit(1)

    print("=" * 60)
    print("SOURCE PROGRAM")
    print("=" * 60)
    print(source)

    # ── Lexical analysis (From lexer.py) ──────────────────────
    token_list = lex(source)
    print("=" * 60)
    print("TOKEN LIST  (scanner output → parser input)")
    print("=" * 60)
    print(f"{'#':<4} {'Token':<6} {'Lexeme'}")
    print("-" * 40)
    for idx, (tok, lex_) in enumerate(token_list, 1):
        print(f"{idx:<4} {tok:<6} {lex_!r}")
    print(f"\nTotal tokens: {len(token_list)}")

    # ── Parsing ───────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("PARSE TREE")
    print("=" * 60)
    parser = Parser(token_list)
    tree   = parser.parse_program()
    tree.pretty()

    print("\n" + "=" * 60)
    if parser.errors:
        print(f"PARSE FAILED  ({len(parser.errors)} error(s))")
        for e in parser.errors:
            print(" ", e)
    else:
        print("PARSE SUCCESSFUL — no syntax errors.")
    print("=" * 60)

if __name__ == '__main__':
    main()