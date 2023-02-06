## Yet Another BrainF**k Compiler

This repo contains sample compiler for brainf**k  written in Python. It's main purpose was to learn LLVM and write compiler from scratch. (llvmlite)[https://github.com/numba/llvmlite] was used in project to as using python llvm API seemed easier.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Interpreter

```bash
python interpreter.py examples/helloworld.bf
```

### Compiler

```bash
python compiler.py examples/helloworld.bf
```

## Performance

Time was measured on mandelbrot implementation.

```bash
time python interpreter.py examples/mandelbrot.bf
```

|          | Python interpreter | CPP interpreter | CPP interpreter -O3[^1] | llvmlite compiler |
|----------|--------------------|-----------------|-------------------------|-------------------|
| time [s] | 4501.16            | 355,97          | 27,88                   | 3.77              |

[^1]: compiled with -O3 option

### Sources

* [LLVM tutorial](https://llvm.org/docs/tutorial/index.html)
* [llvmlite examples](https://github.com/numba/llvmlite/tree/main/examples)
* [llvmlite docs](https://llvmlite.readthedocs.io/en/latest/index.html)
* [LLVM's getelementptr, by example](https://blog.yossarian.net/2020/09/19/LLVMs-getelementptr-by-example)