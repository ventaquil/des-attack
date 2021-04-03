#!/usr/bin/env python3

from . import cast_8_bit_to_6_bit, Cipher as DES, differential_attack_6_rounds, KeyRandomGenerator, \
    PlaintextRandomGenerator, round_key


def bytearray_to_hex(array):
    return "".join("{:0>2X}".format(x) for x in array)


def encryption_decryption():
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

    print("difference  = {0} (same in {1}%)".format(bytearray_to_hex(difference_), round(
        sum([(1 if d == d_ else 0) for d, d_ in zip(difference, difference_)]) / len(difference) * 100)))
    print("ciphertext  = " + bytearray_to_hex(ciphertext))
    print("ciphertext' = " + bytearray_to_hex(ciphertext_))
    print("ciphertext  = {0} (final)".format(bytearray_to_hex(final_ciphertext)))
    print("decrypted   = {0} ({1})".format(bytearray_to_hex(decrypted_plaintext),
                                           "valid" if plaintext == decrypted_plaintext else "invalid"))


def break_6_rounds():
    key = KeyRandomGenerator().generate()
    cipher = DES(key)
    attempts = 512  # how many repeat attack
    round_6_key = round_key(6, key)
    print("Valid key: " + str(cast_8_bit_to_6_bit(round_6_key)))
    difference = bytearray([0x40, 0x08, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00])
    subkeys = [1, 4, 5, 6, 7]  # which sboxes we attack
    possible_keys = differential_attack_6_rounds(cipher, difference, attempts, subkeys)
    round_6_key_candidate = [key[0]["key"] if len(key) > 0 else -1 for key in possible_keys]
    print("Key candidate: " + str(round_6_key_candidate))
    difference = bytearray([0x00, 0x20, 0x00, 0x08, 0x00, 0x00, 0x04, 0x00])
    subkeys = [0, 1, 3, 4, 5]  # which sboxes we attack
    possible_keys = differential_attack_6_rounds(cipher, difference, attempts, subkeys)
    round_6_key_candidate = [key[0]["key"] if len(key) > 0 else -1 for key in possible_keys]
    print("Key candidate: " + str(round_6_key_candidate))


def main():
    print("Encryption/decryption")
    encryption_decryption()
    print("6-round attack")
    break_6_rounds()


if __name__ == "__main__":
    main()
