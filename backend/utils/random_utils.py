import random

def rand_bytes(size: int) -> int:
    """
    Generate a random integer of a specific byte size.

    Args:
        size (int): The size of the random integer in bytes.

    Returns:
        int: A random integer.
    """
    return int.from_bytes(random.randbytes(size), byteorder='little')
