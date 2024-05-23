import random


def rand_bytes(size: int):
    return int.from_bytes(random.randbytes(size), byteorder='little')
