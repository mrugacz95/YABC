import argparse

from generators.llvm_generator import LLVMGenerator
from lexer import Lexer
from parser import Parser, ExprBlock

DEFAULT_CHARSET = "><+-.,[]"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sourcefile")
    parser.add_argument("--charset", default=DEFAULT_CHARSET, required=False)
    args = parser.parse_args()
    source_file = args.sourcefile
    sourcecode = open(source_file, 'r').read()

    charset = args.charset
    if charset != DEFAULT_CHARSET:
        for source_char, default_char in zip(charset, DEFAULT_CHARSET):
            sourcecode = sourcecode.replace(source_char, default_char)

    tokens = Lexer(sourcecode).tokenize()
    ast: ExprBlock = Parser(tokens).parse()

    # generate code
    generator = LLVMGenerator()
    generator.generate(ast)
    generator.run()


if __name__ == '__main__':
    main()
