#!/usr/bin/env python3
from des import Cipher as DES, KeyRandomGenerator, PlaintextRandomGenerator

def bytearray_to_hex(array):
    return "".join("{:0>2X}".format(x) for x in array)

if __name__ == "__main__":
    plaintext = PlaintextRandomGenerator().generate()
    key = KeyRandomGenerator().generate()

    print("plaintext  = " + bytearray_to_hex(plaintext))
    print("key        = " + bytearray_to_hex(key))

    des = DES(key)
    ciphertext = des.encrypt(plaintext)
    decrypted_plaintext = des.decrypt(ciphertext)

    print ("ciphertext = " + bytearray_to_hex(ciphertext))

    print("Test: " + ("It works" if plaintext == decrypted_plaintext else "Failed"))
