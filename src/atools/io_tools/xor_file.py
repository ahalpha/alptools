import itertools


def xor_file(buf: bytes, key: bytes | list[int]):
    return bytes(b ^ k for b, k in zip(buf, itertools.cycle(key)))
