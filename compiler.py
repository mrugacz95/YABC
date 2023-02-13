import argparse
from typing import List

from generators.c_generator import CGenerator
from generators.llvm_generator import LLVMGenerator
from lexer import Lexer
from optimisers.OffsetFuser import OffsetFuser
from optimisers.OperationFuser import OperationFuser
from optimisers.optimiser import Optimiser
from parser import Parser, ExprBlock

DEFAULT_CHARSET = "><+-.,[]"
C_GENERATOR = "c"
LLVM_GENERATOR = "llvm"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sourcefile")
    parser.add_argument("--charset", default=DEFAULT_CHARSET, required=False)
    parser.add_argument("--generator", default=LLVM_GENERATOR, required=False,
                        choices=[C_GENERATOR, LLVM_GENERATOR])
    args = parser.parse_args()
    if args.generator == C_GENERATOR:
        generator = CGenerator()
    else:
        generator = LLVMGenerator()
    source_file = args.sourcefile
    sourcecode = open(source_file, 'r').read()

    charset = args.charset
    if charset != DEFAULT_CHARSET:
        for source_char, default_char in zip(charset, DEFAULT_CHARSET):
            sourcecode = sourcecode.replace(source_char, default_char)

    tokens = Lexer(sourcecode).tokenize()
    ast: ExprBlock = Parser(tokens).parse()

    OperationFuser().optimise(ast)
    OffsetFuser().optimise(ast)

    # generate code
    generator.generate(ast)
    generator.run()


if __name__ == '__main__':
    main()
