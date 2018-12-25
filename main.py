#!/usr/bin/env python3
from des import Cipher as DES, KeyRandomGenerator, PlaintextRandomGenerator

def bytearray_to_hex(array):
    return "".join("{:0>2X}".format(x) for x in array)

if __name__ == "__main__":
    difference = bytearray([0x40, 0x08, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00])
    plaintext, plaintext_ = PlaintextRandomGenerator().generate(difference)
    key = KeyRandomGenerator().generate()

    print("difference  = " + bytearray_to_hex(difference))
    print("plaintext   = " + bytearray_to_hex(plaintext))
    print("plaintext'  = " + bytearray_to_hex(plaintext_))
    print("key         = " + bytearray_to_hex(key))

    des = DES(key)

    final_ciphertext = des.encrypt(plaintext)

    left, right = (plaintext[:4], plaintext[4:])
    left_, right_ = (plaintext_[:4], plaintext_[4:])
    for round_no in range(3):
        round_no += 1
        right, left = des._round(round_no, left, right)
        right_, left_ = des._round(round_no, left_, right_)
    ciphertext = right + left
    ciphertext_ = right_ + left_

    decrypted_plaintext = des.decrypt(final_ciphertext)

    difference_ = bytearray(c0 ^ c1 for c0, c1 in zip(ciphertext, ciphertext_))

    print("difference  = {0} (same in {1}%)".format(bytearray_to_hex(difference_), round(sum([(1 if d == d_ else 0) for d, d_ in zip(difference, difference_)]) / len(difference) * 100)))
    print("ciphertext  = " + bytearray_to_hex(ciphertext))
    print("ciphertext' = " + bytearray_to_hex(ciphertext_))
    print("ciphertext  = {0} (final)".format(bytearray_to_hex(final_ciphertext)))
    print("decrypted   = {0} ({1})".format(bytearray_to_hex(decrypted_plaintext), "valid" if plaintext == decrypted_plaintext else "invalid"))
