import sys
from itertools import islice


def log_error(message):
    print(message, file=sys.stderr)


def window(seq, n=2):
    """
    Returns a sliding window (of width n) over data from the iterable
       s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...
    Source: https://stackoverflow.com/a/6822773/5342020
    """
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result
