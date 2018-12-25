#!/usr/bin/env python3
from math import ceil, log2
import random

class KeyRandomGenerator:
    def generate(self):
        def set_parity(byte):
            parity = True
            for i in range(1, 8): # skip first bit
                parity = not parity if ((byte & (1 << i)) != 0) else parity

            if parity:
                byte |= 1
            else:
                byte &= 0xFE

            return byte

        key = random.randint(0, 2 ** 64 - 1)
        key = "{:0>16x}".format(key)
        key = bytearray.fromhex(key)

        key = bytearray(set_parity(byte) for byte in key)

        return key

class PlaintextRandomGenerator:
    def generate(self, difference=None):
        # TODO validate difference

        plaintext = random.randint(0, 2 ** 64 - 1)
        plaintext = "{:0>16x}".format(plaintext)
        plaintext = bytearray.fromhex(plaintext)

        if difference == None:
            return plaintext

        plaintext = (
            plaintext,
            bytearray(p ^ d for p, d in zip(plaintext, difference))
        )

        return plaintext

class Sbox:
    def __init__(self, pattern):
        self.pattern = pattern

    def __call__(self, row, column):
        return self.pattern[row][column]

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, pattern):
        # TODO validation
        self._pattern = pattern

class LinearTransformation:
    def __init__(self, pattern):
        self.pattern = pattern

    def __call__(self, bytes):
        if type(bytes) is not bytearray:
            raise Exception("Input data is not bytearray")

        #if ((len(bytes) * 8) < len(self.pattern)) or ((len(bytes) * 8) < max(self.pattern)):
        #    raise Exception("Input data length not match to pattern length")

        def get_bit(byte, no):
            no = (8 - no) - 1

            return (byte & (1 << no)) >> no

        def set_bit(byte, no, value):
            no = (8 - no) - 1

            if value == 1:
                byte |= 1 << no
            else:
                byte &= 0xFF ^ (1 << no)

            return byte

        size = len(self.pattern) // 8

        transformated = [0] * size
        for i in range(size):
            for (j, k) in zip(self.pattern[i * 8:(i + 1) * 8], range(8)):
                if j > 0:
                    j -= 1 # decrement because values start from 1
                    byte = bytes[j // 8]
                    bit = get_bit(byte, j % 8)
                    transformated[i] = set_bit(transformated[i], k, bit)

        return bytearray(transformated)

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, pattern):
        if type(pattern) not in [list, tuple]:
            raise Exception("Pattern must be list or tuple")

        if (len(pattern) % 8) != 0:
            raise Exception("Pattern length must be multiple of 8")

        for value in pattern:
            if type(value) is not int:
                raise Exception("Pattern must contains positive integers")

            #if value > len(pattern):
            #    raise Exception("Values in pattern cannot be greater than pattern length")

            if value < 0:
                raise Exception("Values in pattern cannot be smaller than 0")

        self._pattern = pattern

def function_e(data):
    e = LinearTransformation((32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1))

    return e(data)

def function_k(data, key):
    return bytearray([d ^ k for (d, k) in zip(data, key)])

def initial_permutation(data):
    ip = LinearTransformation((58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7))

    return ip(data)

def initial_permutation_inverted(data):
    ip_inv = LinearTransformation((40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25))

    return ip_inv(data)

def pc1(key):
    c = (57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36)
    d = (63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4)

    pc1 = LinearTransformation(c + d)

    return pc1(key)

def pc2(key):
    pc2 = LinearTransformation((14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32))

    return pc2(key)

def permutation(data):
    p = LinearTransformation((16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25))

    return p(data)

def round_key(no, key):
    def rotate(array, rotation):
        result = [0] * len(array)
        for i in range(len(array)):
            result[i] = array[i] << rotation
            result[i] |= (array[(i + 1) % len(array)] >> (4 - rotation))
            result[i] &= 0x0F
        return result

    key = pc1(key)

    rotations = (1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1)

    halfbytes = []
    for byte in key:
        halfbytes.append((byte & 0xF0) >> 4)
        halfbytes.append(byte & 0x0F)

    c = halfbytes[:7]
    d = halfbytes[7:]

    for rotation in rotations[:no]:
        c = rotate(c, rotation)
        d = rotate(d, rotation)

    halfbytes = c + d

    key = [(c << 4) | d for (c, d) in zip(halfbytes[::2], halfbytes[1::2])]
    key = bytearray(key)

    return pc2(key)

def sboxes(data):
    def combine_bits(bits):
        combined = 0
        for (i, j) in zip(reversed(range(len(bits))), range(len(bits))):
            combined |= bits[i] << j
        return combined

    def get_bit(byte, no):
        shift = 6 - no
        return (byte & (1 << shift)) >> shift

    def get_column(byte):
        bits = list(range(2, 6))
        return combine_bits([get_bit(byte, bit) for bit in bits])

    def get_row(byte):
        bits = [1, 6]
        return combine_bits([get_bit(byte, bit) for bit in bits])

    sboxes = [
        [
            (14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7), 
            (0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8), 
            (4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0), 
            (15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13)
        ],
        [
            (15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10),
            (3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5),
            (0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15),
            (13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9)
        ],
        [
            (10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8),
            (13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1),
            (13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7),
            (1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12)
        ],
        [
            (7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15),
            (13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9),
            (10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4),
            (3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14)
        ],
        [
            (2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9),
            (14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6),
            (4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14),
            (11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3)
        ],
        [
            (12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11),
            (10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8),
            (9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6),
            (4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13)
        ],
        [
            (4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1),
            (13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6),
            (1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2),
            (6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12)
        ],
        [
            (13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7),
            (1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2),
            (7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8),
            (2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11)
        ]
    ]

    sboxes = [Sbox(pattern) for pattern in sboxes]

    sboxed = [0] * 4

    byte = 0 # start from 0 byte
    bit = 6 # get 6 bits (counting from 1)

    for i in range(0, len(data) * 8, 6):
        sbox = i // 6

        value = data[byte] >> (8 - bit)
        if bit < 6:
            value |= data[byte - 1] << bit
        value &= 0x3F

        result = sboxes[sbox](get_row(value), get_column(value))

        sboxed[sbox // 2] |= result << (4 * ((sbox + 1) % 2))

        bit += 6

        if bit > 8:
            bit %= 8
            byte += 1

    return bytearray(sboxed)

class Cipher:
    def __init__(self, key):
        self.key = key if type(key) is bytearray else bytearray(key)
        self.rounds = 16

    def encrypt(self, message):
        def divide(block):
            return (block[:4], block[4:])

        message = initial_permutation(message)

        left, right = divide(message)

        for round in range(self.rounds):
            round += 1 # increment to use values from 1

            right, left = self._round(round, left, right)

        return initial_permutation_inverted(right + left)

    def decrypt(self, message):
        def divide(block):
            return (block[:4], block[4:])

        message = initial_permutation(message)

        left, right = divide(message)

        for round in range(self.rounds):
            right, left = self._round(self.rounds - round, left, right)

        return initial_permutation_inverted(right + left)

    def f(self, data, key):
        expanded = function_e(data)

        keyed = function_k(expanded, key)

        substituted = sboxes(keyed)

        permuted = permutation(substituted)

        return permuted

    def _round(self, no, left, right):
        key = round_key(no, self.key)

        left = bytearray([l ^ r for (l, r) in zip(left, self.f(right, key))])

        return (left, right)
