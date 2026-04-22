This is a professional README file tailored for your GitHub repository. It clearly explains the project, the grammar, and most importantly, the two different lexing strategies you've implemented.
Mini-JavaScript Recursive-Descent Parser
Group 19 - Compiler Construction
This project implements a complete Lexical Analyzer (Lexer) and a Recursive-Descent Predictive Parser for a subset of JavaScript. The system transforms raw source code into a structured Parse Tree.
🚀 Project Overview
The project is divided into two main components:
Lexer (lexer.py): A state-machine-based tokenizer that converts raw text into tokens (Keywords, Identifiers, Numbers, and Operators).
Parser (parser.py): A predictive parser that validates the token stream against the Mini-JavaScript context-free grammar and generates a visual Parse Tree.
⚖️ The Two Lexing Strategies
This repository contains two versions of the Lexer to demonstrate different approaches to formal language theory.
1. Pure DFA Version (Keyword Priority)
This version follows a strict Deterministic Finite Automaton (DFA) model without using delimiters or lookahead to terminate tokens.
Behavior: Keywords (let, if, while) are given absolute priority in the state transition table.
The "Splitting" Effect: Because the DFA stops immediately upon reaching a Keyword state, a string like letter will be lexed as KW('let') followed by ID('ter').
Use Case: Specifically designed to meet academic requirements where tokenization must be driven purely by state transitions rather than whitespace delimiters.
2. Standard Version (Maximal Munch)
This version implements the industry-standard Maximal Munch (Longest Match) principle used in production compilers (like GCC or V8).
Behavior: The lexer continues to consume characters as long as they form a valid Identifier, even if a substring matches a Keyword.
The Logic: letter is lexed as a single ID('letter').
Use Case: Practical programming language design where variable names are allowed to contain keyword substrings.
📜 Supported Grammar
The parser supports the following Mini-JS grammar:
code
Antlr
program     → stmt_list
stmt_list   → stmt stmt_list | ε
stmt        → let_stmt | if_stmt | while_stmt | assign_stmt
let_stmt    → 'let' ID '=' expr ';'
assign_stmt → ID '=' expr ';'
if_stmt     → 'if' '(' cond ')' '{' stmt_list '}'
while_stmt  → 'while' '(' cond ')' '{' stmt_list '}'
cond        → expr '<' expr
expr        → term expr_tail
expr_tail   → '+' term expr_tail | ε
term        → NUM | ID
🛠️ Installation & Usage
Clone the repository:
code
Bash
git clone https://github.com/your-username/mini-js-parser.git
cd mini-js-parser
Run the Parser:
Place your source code in a file (e.g., sample.js) and run:
code
Bash
python parser.py sample.js
📂 Project Structure
lexer.py: Contains the DFA state machine and the lex() function.
parser.py: Contains the Parser class, the Node class for tree generation, and the main execution logic.
sample.js: A sample Mini-JS file for testing.
📝 Example Output
Input (sample.js):
code
JavaScript
let sum = 0;
while (sum < 10) {
    sum = sum + 1;
}
Output (Parse Tree):
code
Text
program
└── stmt_list
    ├── stmt
    │   └── let_stmt
    │       ├── 'let'  [KW: 'let']
    │       ├── ID  [ID: 'sum']
    │       ├── '='  [OP: '=']
    │       ├── expr
    │       │   ├── term
    │       │   │   └── NUM  [NUM: '0']
    │       │   └── expr_tail
    │       │       └── ε
    │       └── ';'  [OP: ';']
    └── stmt_list
        └── ...
Contributors: Group 19 - Compiler Construction Class.
