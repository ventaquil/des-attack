#!/usr/bin/env python3
from DES import DES
import random

def rand_message():
    message = random.randint(0, 2 ** 64 - 1)
    message = "{:0>16x}".format(message)
    message = bytearray.fromhex(message)
    return message

def rand_key():
    def set_parity(byte):
        parity = True
        for i in range(1, 8):
            parity = not parity if ((byte & (1 << i)) != 0) else parity

        if parity:
            byte |= 1

        return byte

    key = random.randint(0, 2 ** 64 - 1)
    key = "{:0>16x}".format(key)
    key = bytearray.fromhex(key)

    key = bytearray([set_parity(byte) for byte in key])

    return key

if __name__ == "__main__":
    message = rand_message()
    key = rand_key()

    des = DES(key, message)
    for i in range(1, 7):
        des.round(i)

    des = DES(key, des.ciphertext)
    for i in range(1, 7):
        des.round(i)

    print(message == des.ciphertext)
