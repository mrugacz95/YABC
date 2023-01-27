import sys
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sourcefile")
    args = parser.parse_args()
    source_file = args.sourcefile
    sourcecode = open(source_file, 'r').read()

    # preprocessing
    available_chars = '<>[].,+-'
    code = [c for c in sourcecode if c in available_chars]

    # analyse brackets
    stack = []
    jump_forward = {}
    jump_backward = {}
    for program_counter, op in enumerate(code):
        if code[program_counter] == '[':
            stack.append(program_counter)
        elif code[program_counter] == ']':
            open_bracket_pos = stack.pop()
            jump_forward[open_bracket_pos] = program_counter
            jump_backward[program_counter] = open_bracket_pos
        program_counter += 1

    # initialization
    mem = [0] * 3000
    ptr = 0
    program_counter = 0

    def inc_ptr():
        nonlocal ptr
        ptr += 1

    def dec_ptr():
        nonlocal ptr
        ptr -= 1

    def start_loop():
        nonlocal program_counter
        if mem[ptr] == 0:
            program_counter = jump_forward[program_counter]

    def end_loop():
        nonlocal program_counter
        program_counter = jump_backward[program_counter] - 1

    def inc_value():
        mem[ptr] += 1

    def dec_value():
        mem[ptr] -= 1

    def print_char():
        print(chr(mem[ptr]), end='')

    def write_char():
        nonlocal ptr
        char = sys.stdin.read(1)
        mem[ptr] = ord(char)

    while program_counter < len(code):
        op = code[program_counter]
        {
            '>': inc_ptr,
            '<': dec_ptr,
            '[': start_loop,
            ']': end_loop,
            '+': inc_value,
            '-': dec_value,
            '.': print_char,
            ',': write_char
        }.get(op)()
        program_counter += 1


if __name__ == '__main__':
    main()
