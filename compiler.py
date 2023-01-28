import argparse

from lexer import Lexer
from parser import Parser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sourcefile")
    args = parser.parse_args()
    source_file = args.sourcefile
    sourcecode = open(source_file, 'r').read()

    tokens = Lexer(sourcecode).tokenize()
    ast = Parser(tokens).parse()

    # todo generate IR code

if __name__ == '__main__':
    main()