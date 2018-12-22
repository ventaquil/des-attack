#!/usr/bin/env python3
from des import Cipher as DES, random_message, random_key

def message_from_differential(original, differential):
    differential = "{:0>16}".format(differential)
    differential = bytearray.fromhex(differential)

    return bytearray([m ^ d for (m, d) in zip(original, differential)])

def bytearray_to_hex(array):
    return "".join("{:0>2x}".format(x) for x in array)

if __name__ == "__main__":
    message = random_message()
    key = random_key()
    differential = "2000000000000caf"

    print("message      = " + bytearray_to_hex(message))
    print("message'     = " + bytearray_to_hex(message_from_differential(message, differential)))
    print("differential = " + differential)
    print("key          = " + bytearray_to_hex(key))

    des = DES(key)
    ciphertext = des.encrypt(message)
    plaintext = des.decrypt(ciphertext)

    print("Test: " + ("It works" if message == plaintext else "Failed"))
