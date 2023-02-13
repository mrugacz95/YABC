from lexer import Lexer, Token


def test_lexer():
    test_code = ',++>++++[-<+>].'
    tokenized = Lexer(test_code).tokenize()
    assert tokenized == [Token.SCAN, Token.INC_VAL, Token.INC_VAL,
                         Token.INC_PTR, Token.INC_VAL, Token.INC_VAL,
                         Token.INC_VAL, Token.INC_VAL, Token.L_BRACKET,
                         Token.DEC_VAL, Token.DEC_PTR, Token.INC_VAL,
                         Token.INC_PTR, Token.R_BRACKET, Token.PRINT,
                         Token.EOF]
