import argparse
from ctypes import CFUNCTYPE, c_int

from llvmlite import ir
from llvmlite.ir import Function

from lexer import Lexer
from llvm_helpers import compile_ir, create_execution_engine
from parser import Parser, ExprBlock


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sourcefile")
    args = parser.parse_args()
    source_file = args.sourcefile
    sourcecode = open(source_file, 'r').read()

    tokens = Lexer(sourcecode).tokenize()
    ast: ExprBlock = Parser(tokens).parse()

    int = ir.IntType(8)
    fnty = ir.FunctionType(int, ())

    module = ir.Module(name="bfk_module")

    func = ir.Function(module, fnty, name="main")
    block = func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)

    stackint = builder.alloca(ir.IntType(8))
    builder.store(ir.Constant(stackint.type.pointee, 123), stackint)
    acc = builder.load(stackint)

    ptr_u8 = ir.PointerType(ir.IntType(8))
    f_u8_u8 = ir.FunctionType(int, (ptr_u8,))
    puts = ir.Function(module, f_u8_u8, name="puts")
    builder.call(puts, (stackint,))
    builder.ret(acc)

    mod = str(module)
    print(mod)

    engine = create_execution_engine()
    compile_ir(engine, mod)

    func_ptr = engine.get_function_address("main")

    # Run the function via ctypes
    cfunc = CFUNCTYPE(c_int)(func_ptr)
    ret = cfunc()
    print(f"Finished with {ret}")


if __name__ == '__main__':
    main()
