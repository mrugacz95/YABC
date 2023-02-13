from lexer import Token
from parser import Parser, ExprChangePtr, ExprLoop, ExprBlock, ExprScan, \
    ExprPrint, ExprChangeValue


def test_parser():
    test_code = [Token.INC_PTR, Token.INC_PTR, Token.L_BRACKET,
                 Token.SCAN, Token.PRINT, Token.R_BRACKET, Token.INC_VAL,
                 Token.DEC_VAL, Token.EOF]
    parsed = Parser(test_code).parse()
    expected = ExprBlock([
        ExprChangePtr(1), ExprChangePtr(1), ExprLoop(
            ExprBlock(
                [
                    ExprScan(),
                    ExprPrint(),
                ]
            )),
        ExprChangeValue(offset=0, value=1),
        ExprChangeValue(offset=0, value=-1)
    ])
    assert parsed == expected
