"""
Lexical Analyzer for Mini-JavaScript Grammar
Group 19 - Compiler Construction

NOTE: This version prioritizes Keywords. 
Example: 'lets' is lexed as 'let' (KW) followed by 's' (ID).
"""

import string

# DFA Transitions for keywords: let, if, while
_KW_TRANSITIONS = {
    'A': {'l': 'B', 'i': 'C', 'w': 'D'},
    'B': {'e': 'H'},
    'C': {'f': 'I'},
    'D': {'h': 'J'},
    'H': {'t': 'K'},
    'J': {'i': 'L'},
    'L': {'l': 'M'},
    'M': {'e': 'N'},
}

_LETTERS   = set(string.ascii_letters + '_')
_DIGITS    = set(string.digits)
_ID_CHARS  = _LETTERS | _DIGITS
_OP_CHARS  = set('=+<(){};')

_ACCEPTING = {
    'B': 'ID', 'C': 'ID', 'D': 'ID',
    'H': 'ID', 'J': 'ID', 'L': 'ID', 'M': 'ID',
    'E': 'ID',
    'I': 'KW', 'K': 'KW', 'N': 'KW',
    'F': 'NUM',
    'G': 'OP',
}

def _next_state(state, char):
    if state in _KW_TRANSITIONS and char in _KW_TRANSITIONS[state]:
        return _KW_TRANSITIONS[state][char]
    if state == 'A':
        if char in _LETTERS: return 'E'
        if char in _DIGITS:  return 'F'
        if char in _OP_CHARS: return 'G'
    elif state in ('B','C','D','H','J','L','M'):
        # If we are in a partial keyword path and get a non-matching ID char
        if char in _ID_CHARS: return 'E'
    elif state in ('E','I','K','N'):
        if char in _ID_CHARS: return 'E'
    elif state == 'F':
        if char in _DIGITS: return 'F'
    return None

def lex(source):
    """
    Converts source code into tokens.
    Implements Keyword Priority: stops as soon as a KW is recognized.
    """
    tokens = []
    i = 0
    n = len(source)
    
    while i < n:
        # Skip whitespace
        if source[i].isspace():
            i += 1
            continue
            
        state = 'A'
        last_acc_state = None
        last_acc_pos   = -1
        j = i
        
        while j < n:
            nxt = _next_state(state, source[j])
            if nxt is None:
                break
            
            state = nxt
            if state in _ACCEPTING:
                last_acc_state = state
                last_acc_pos   = j
                
                # PRIORITY LOGIC: 
                # If we hit a Keyword, we stop immediately.
                # 'let' will be captured as KW even if the next char is 's'
                if _ACCEPTING[state] == 'KW':
                    break 
            j += 1
            
        if last_acc_state is not None:
            lexeme   = source[i:last_acc_pos + 1]
            tok_type = _ACCEPTING[last_acc_state]
            tokens.append((tok_type, lexeme))
            i = last_acc_pos + 1
        else:
            # Handle unknown characters
            tokens.append(('ERR', source[i]))
            i += 1
            
    tokens.append(('EOF', '$'))
    return tokens