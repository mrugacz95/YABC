import argparse
from ctypes import CFUNCTYPE, c_int

from llvmlite import ir

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

    int32 = ir.IntType(32)
    int64 = ir.IntType(64)
    void_type = ir.VoidType()

    module = ir.Module(name="bfk_module")

    # execution variable
    mem = ir.GlobalVariable(module, ir.ArrayType(ir.IntType(32), 3000), "mem")  # int mem[3000]
    mem.linkage = "common"
    mem.initializer = ir.Constant(ir.ArrayType(ir.IntType(32), 3000), None)

    # external functions
    putchar_type = ir.FunctionType(int32, [int32])
    putchar = ir.Function(module, putchar_type, name="putchar")
    getchar_type = ir.FunctionType(int32, [])
    getchar = ir.Function(module, getchar_type, name="getchar")

    # main function
    main_type = ir.FunctionType(int32, ())
    func = ir.Function(module, main_type, name="main")
    block = func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)

    # ptr = ir.GlobalVariable(module, ir.PointerType(ir.IntType(32), mem), "ptr")

    ptr = builder.alloca(ir.PointerType(int32), name="ptr")
    builder.store(builder.gep(mem, [ir.Constant(int32, 0), ir.Constant(int32, 0)]), ptr)

    #  generate code
    ast.codegen(builder, mem, ptr, putchar, getchar)

    builder.ret(ir.Constant(int32, 0))

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
