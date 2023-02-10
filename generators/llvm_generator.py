from llvmlite import ir
from ctypes import CFUNCTYPE, c_int
from llvm_helpers import create_execution_engine, compile_ir
from parser import ExprLoop, ExprChangeValue, ExprPrint, ExprScan, ExprDecreasePtr, \
    ExprIncreasePtr, ExprBlock, ExprAST
from utils import log_error
from generators.generator import ASTGenerator


class LLVMGenerator(ASTGenerator):

    def __init__(self):
        self.int32 = ir.IntType(32)

        self.module = ir.Module(name="bfk_module")

        # execution variable
        self.mem = ir.GlobalVariable(self.module, ir.ArrayType(self.int32, 3000), "mem")  # int mem[3000]
        self.mem.linkage = "common"
        self.mem.initializer = ir.Constant(ir.ArrayType(self.int32, 3000), None)

        # external functions
        putchar_type = ir.FunctionType(self.int32, [self.int32])
        self.putchar = ir.Function(self.module, putchar_type, name="putchar")
        getchar_type = ir.FunctionType(self.int32, [])
        self.getchar = ir.Function(self.module, getchar_type, name="getchar")

        # main function
        main_type = ir.FunctionType(self.int32, ())
        fun_main = ir.Function(self.module, main_type, name="main")
        block = fun_main.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        # init mem pointer
        self.ptr = self.builder.alloca(ir.PointerType(self.int32), name="ptr")
        self.builder.store(self.builder.gep(self.mem, [ir.Constant(self.int32, 0), ir.Constant(self.int32, 0)]),
                           self.ptr)

    def generate(self, ast: ExprAST):

        self._visit(self.builder, ast)

        # return 0
        self.builder.ret(ir.Constant(self.int32, 0))

    def run(self):
        mod = str(self.module)

        engine = create_execution_engine()
        compile_ir(engine, mod)

        func_ptr = engine.get_function_address("main")

        # Run the function via ctypes
        cfunc = CFUNCTYPE(c_int)(func_ptr)
        ret = cfunc()
        if ret != 0:
            log_error(f"Finished with {ret}")

    def _visitIncreasePtr(self, builder, expr: ExprIncreasePtr):
        ptr_addr = builder.load(self.ptr)
        new_addr = builder.gep(ptr_addr, [ir.Constant(ir.IntType(32), expr.value)])
        builder.store(new_addr, self.ptr)

    def _visitDecreasePtr(self, builder, expr: ExprDecreasePtr):
        ptr_addr = builder.load(self.ptr)
        new_addr = builder.gep(ptr_addr, [ir.Constant(ir.IntType(32), -expr.value)])
        builder.store(new_addr, self.ptr)

    def _visitChangeValue(self, builder, expr: ExprChangeValue):
        ptr_addr = builder.load(self.ptr)
        value = builder.load(ptr_addr)
        res = builder.add(value, ir.Constant(ir.IntType(32), expr.value))
        builder.store(res, ptr_addr)

    def _visitLoop(self, builder, expr: ExprLoop):
        loop_cond = builder.append_basic_block("loop_cond")
        loop_builder = builder.append_basic_block("loop_block")
        loop_end = builder.append_basic_block("loop_end")

        # condition
        cond_builder = ir.IRBuilder(loop_cond)
        ptr_addr = cond_builder.load(self.ptr)
        value = cond_builder.load(ptr_addr)
        cond = cond_builder.icmp_signed("!=", value, ir.Constant(ir.IntType(32), 0))
        cond_builder.cbranch(cond, loop_builder, loop_end)

        # loop block
        loop_builder = ir.IRBuilder(loop_builder)

        self._visitBlock(loop_builder, expr.block)

        loop_builder.branch(loop_cond)

        # lop end
        builder.branch(loop_cond)
        builder.position_at_end(loop_end)

    def _visitScan(self, builder, expr: ExprScan):
        tmp = builder.call(self.getchar, ())
        ptr_addr = builder.load(self.ptr)
        builder.store(tmp, ptr_addr)

    def _visitPrint(self, builder, expr: ExprPrint):
        ptr_addr = builder.load(self.ptr)
        value = builder.load(ptr_addr)
        builder.call(self.putchar, (value,))

    def _visitBlock(self, builder, expr: ExprBlock):
        for inner_expression in expr.expressions:
            self._visit(builder, inner_expression)
