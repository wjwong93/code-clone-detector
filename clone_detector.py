import sys
from antlr4 import *
from Python3Lexer import Python3Lexer
import TokenTypes
from collections import deque

def generate_token_list(source_file, output_file=False):
    # Returns list of tokens from source code
    with open(source_file, 'r') as file:
        source = file.read()

    input = InputStream(source)
    lexer = Python3Lexer(input)
    tokens = CommonTokenStream(lexer)
    tokens.fill()

    res = []

    if output_file:
        file = open(f'{source_file}-tokenised.txt', 'w')

    for i in range(len(tokens.tokens)):
        token = tokens.get(i)
        res.append(token)

        if output_file:
            file.write(f'{TokenTypes.token_types[token.type]} {token.text}\n')

    if output_file:
        file.close()

    return res

def print_token_list(token_list):
    for token in token_list:
        print(f"({token.type}, {repr(token.text)})", end=' ')
    print()

def isEqualToken(token1, token2):
    if token1.type == token2.type and token1.text == token2.text:
        return True
    return False

def isType1Clone(list1, list2):
    m, n = len(list1), len(list2)
    if m != n:
        return False

    for i in range(m):
        if not isEqualToken(list1[i], list2[i]):
            return False

    return True

def ignore_var_and_literals(token_list):
        literals = [
            3, # STRING
            4 # NUMBER
        ]
        variables = [
            42 # NAME
        ]

        for t in token_list:
            if t.type in literals:
                t.text = "L"
            elif t.type in variables:
                t.text = "V"

        return token_list

def isType2Clone(list1, list2):
    list1, list2 = ignore_var_and_literals(list1), ignore_var_and_literals(list2)

    m, n = len(list1), len(list2)
    if m != n:
        return False

    for i in range(m):
        if not isEqualToken(list1[i], list2[i]):
            print(list1[i].type, list2[i].type)
            return False

    return True

def lcs(list1, list2):
    # Return length of lcs
    m, n = len(list1), len(list2)
    memo = [ [ (0, deque(), deque()) for _ in range(n+1) ] for _ in range(m+1) ]
            
    for i in range(m-1, -1, -1):
        for j in range(n-1, -1, -1):
            # print(i, j, memo[0][0][0], memo[0][0][1])
            if isEqualToken(list1[i], list2[j]):
                new_deque1 = memo[i+1][j+1][1].copy()
                new_deque1.appendleft(list1[i])
                new_deque2 = memo[i+1][j+1][2].copy()
                new_deque2.appendleft(list2[j])
                memo[i][j] = (
                    memo[i+1][j+1][0] + 1,
                    new_deque1,
                    new_deque2
                )

            else:
                if memo[i+1][j][0] > memo[i][j+1][0]:
                    memo[i][j] = memo[i+1][j]

                else:
                    memo[i][j] = memo[i][j+1]


    return memo[0][0]

def isType3Clone(list1, list2, gap=5):
    list1, list2 = ignore_var_and_literals(list1), ignore_var_and_literals(list2)
    lcs_len, lcs_tokens1, lcs_tokens2 = lcs(list1, list2)
    if lcs_len < 2:
        return False

    lcs_tokens1, lcs_tokens2 = list(lcs_tokens1), list(lcs_tokens2)
    for i in range(lcs_len - 1):
        if lcs_tokens1[i+1].tokenIndex - lcs_tokens1[i].tokenIndex > gap:
            return False

    for i in range(lcs_len - 1):
        if lcs_tokens2[i+1].tokenIndex - lcs_tokens2[i].tokenIndex > gap:
            return False

    return True

src1 = 'samples/matplotlib/sample3-1.py'
src2 = 'samples/matplotlib/sample3-2.py'

tokens1 = generate_token_list(src1)
tokens2 = generate_token_list(src2)

print('Source 1: ', len(tokens1))
print('Source 2: ', len(tokens2))
result = lcs(tokens1, tokens2)

print('LCS Length: ', result[0])

print('Is Type 1 Clone: ', isType1Clone(tokens1, tokens2))
print('Is Type 2 Clone: ', isType2Clone(tokens1, tokens2))
print('Is Type 3 Clone: ', isType3Clone(tokens1, tokens2))

# print_token_list(result[2])