"""
Library
"""
from time import time


def ms():
    return round(time()*1000)


def pairs(l):
    """
    Convert list to pairs
    """
    for i in range(0, len(l), 2):
        # Create an index range for l of n items:
        yield (*l[i:i+2],)


def gen_key(uid, section='s'):
    """
    Generate store key for own user
    """
    return f'cs:{section}:{uid}'.encode()
