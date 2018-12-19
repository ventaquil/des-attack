#!/usr/bin/env python3
class DES:
    class KeySchedule:
        @staticmethod
        def round_key(round_no, key):
            def left_rotate(bits, i):
                # TODO implement rotation
                return bits

            C, D = DES.KeySchedule.PC1(key)

            rotations = (1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1)

            for i in range(round_no):
                C = left_rotate(C, rotations[i])
                D = left_rotate(D, rotations[i])

            return DES.KeySchedule.PC2(C, D)

        @staticmethod
        def PC1(key):
            def get_bit(bit_no):
                return (key[bit_no // 8] & (1 << (bit_no % 6))) >> (bit_no % 6)

            def C():
                pattern = ((57, 49, 41, 33, 25, 17, 9),
                    (1, 58, 50, 42, 34, 26, 18),
                    (10, 2, 59, 51, 43, 35, 27),
                    (19, 11, 3, 60, 52, 44, 36))

                chosen = []

                for i in range(4):
                    byte = 0
                    for j in range(6):
                        byte <<= 1
                        byte |= get_bit(pattern[i][j])
                    chosen.append(byte)

                return bytearray(chosen)

            def D(): 
                pattern = ((63, 55, 47, 39, 31, 23, 15),
                    (7, 62, 54, 46, 38, 30, 22),
                    (14, 6, 61, 53, 45, 37, 29),
                    (21, 13, 5, 28, 20, 12, 4))

                chosen = []

                for i in range(4):
                    byte = 0 
                    for j in range(6):
                        byte <<= 1
                        byte |= get_bit(pattern[i][j])
                    chosen.append(byte)

                return bytearray(chosen)

            return (C(), D())

        @staticmethod
        def PC2(C, D):
            def get_bit(bit_no):
                return (data[bit_no // 8] & (1 << (bit_no % 6))) >> (bit_no % 6)

            data = C + D

            pattern = ((14, 17, 11, 24, 1, 5),
                (3, 28, 15, 6, 21, 10),
                (23, 19, 12, 4, 26, 8),
                (16, 7,  27, 20, 13, 2),
                (41, 52, 31, 37, 47, 55),
                (30, 40, 51, 45, 33, 48),
                (44, 49, 39, 56, 34, 53),
                (46, 42, 50, 36, 29, 32))

            chosen = []

            for i in range(8):
                byte = 0
                for j in range(6):
                    byte <<= 1
                    byte |= get_bit(pattern[i][j])
                chosen.append(byte)

            return bytearray(chosen)

    class Transformation:
        @staticmethod
        def E(data):
            def get_bit(i):
                i -= 1
                index = i // 8
                bit = i % 8
                return (data[index] & (1 << bit)) >> bit

            pattern = ((32, 1, 2, 3, 4, 5, 4, 5),
                (6, 7, 8, 9, 8, 9, 10, 11),
                (12, 13, 12, 13, 14, 15, 16, 17),
                (16, 17, 18, 19, 20, 21, 20, 21),
                (22, 23, 24, 25, 24, 25, 26, 27),
                (28, 29, 28, 29, 30, 31, 32, 1))

            expanded = []

            for i in range(len(pattern)):
                byte = 0
                for j in range(len(pattern[i])):
                    byte <<= 1
                    byte |= get_bit(pattern[i][j])
                expanded.append(byte)

            return bytearray(expanded)

        @staticmethod
        def P(data):
            def get_bit(i):
                i -= 1
                index = i // 8
                bit = i % 8
                return (data[index] & (1 << bit)) >> bit

            pattern = (16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25)

            permuted = []

            for i in range(len(pattern) // 8):
                byte = 0
                for j in range(8):
                    byte <<= 1
                    byte |= get_bit(pattern[(i * 8) + j])
                permuted.append(byte)

            return bytearray(permuted)

        @staticmethod
        def S(data):
            def get_bit(bit_no):
                return (data[bit_no // 8] & (1 << (bit_no % 6))) >> (bit_no % 6)

            def get_sbox_method(i):
                methods = (
                    DES.Transformation.S1,
                    DES.Transformation.S2,
                    DES.Transformation.S3,
                    DES.Transformation.S4,
                    DES.Transformation.S5,
                    DES.Transformation.S6,
                    DES.Transformation.S7,
                    DES.Transformation.S8
                )

                return methods[i]

            substituted = []

            bit = 0
            for i in range(8):
                bits = 0
                for j in range(6):
                    bits <<= 1
                    bits |= get_bit(bit)
                    bit += 1

                substituted.append(get_sbox_method(i)(bits))

            substituted = [(substituted[left] << 4) | substituted[right] for (left, right) in zip(range(0, 8, 2), range(1, 8, 2))]

            return bytearray(substituted)

        @staticmethod
        def S1(data):
            def get_bit(bits, i):
                return (bits & (1 << i)) >> (1 << i)

            def combine_bits(bits):
                combined = 0
                for (i, j) in zip(reversed(range(len(bits))), range(len(bits))):
                    combined |= bits[i] << j
                return combined

            def get_no(bits):
                return combine_bits([get_bit(bits, 0), get_bit(bits, 5)])

            def get_row(bits):
                return combine_bits([get_bit(bits, i) for i in range(1, 6)])

            pattern = ((14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7),
                (0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8),
                (4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0),
                (15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13))

            return pattern[get_row(data)][get_no(data)]

        @staticmethod
        def S2(data):
            def get_bit(bits, i):
                return (bits & (1 << i)) >> (1 << i)

            def combine_bits(bits):
                combined = 0
                for (i, j) in zip(reversed(range(len(bits))), range(len(bits))):
                    combined |= bits[i] << j
                return combined

            def get_no(bits):
                return combine_bits([get_bit(bits, 0), get_bit(bits, 5)])

            def get_row(bits):
                return combine_bits([get_bit(bits, i) for i in range(1, 6)])

            pattern = ((15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10),
                (3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5),
                (0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15),
                (13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9))

            return pattern[get_row(data)][get_no(data)]

        @staticmethod
        def S3(data):
            def get_bit(bits, i):
                return (bits & (1 << i)) >> (1 << i)

            def combine_bits(bits):
                combined = 0
                for (i, j) in zip(reversed(range(len(bits))), range(len(bits))):
                    combined |= bits[i] << j
                return combined

            def get_no(bits):
                return combine_bits([get_bit(bits, 0), get_bit(bits, 5)])

            def get_row(bits):
                return combine_bits([get_bit(bits, i) for i in range(1, 6)])

            pattern = ((10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8),
                (13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1),
                (13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7),
                (1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12))

            return pattern[get_row(data)][get_no(data)]

        @staticmethod
        def S4(data):
            def get_bit(bits, i):
                return (bits & (1 << i)) >> (1 << i)

            def combine_bits(bits):
                combined = 0
                for (i, j) in zip(reversed(range(len(bits))), range(len(bits))):
                    combined |= bits[i] << j
                return combined

            def get_no(bits):
                return combine_bits([get_bit(bits, 0), get_bit(bits, 5)])

            def get_row(bits):
                return combine_bits([get_bit(bits, i) for i in range(1, 6)])

            pattern = ((7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15),
                (13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9),
                (10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4),
                (3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14))

            return pattern[get_row(data)][get_no(data)]

        @staticmethod
        def S5(data):
            def get_bit(bits, i):
                return (bits & (1 << i)) >> (1 << i)

            def combine_bits(bits):
                combined = 0
                for (i, j) in zip(reversed(range(len(bits))), range(len(bits))):
                    combined |= bits[i] << j
                return combined

            def get_no(bits):
                return combine_bits([get_bit(bits, 0), get_bit(bits, 5)])

            def get_row(bits):
                return combine_bits([get_bit(bits, i) for i in range(1, 6)])

            pattern = ((2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9),
                (14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6),
                (4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14),
                (11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3))

            return pattern[get_row(data)][get_no(data)]

        @staticmethod
        def S6(data):
            def get_bit(bits, i):
                return (bits & (1 << i)) >> (1 << i)

            def combine_bits(bits):
                combined = 0
                for (i, j) in zip(reversed(range(len(bits))), range(len(bits))):
                    combined |= bits[i] << j
                return combined

            def get_no(bits):
                return combine_bits([get_bit(bits, 0), get_bit(bits, 5)])

            def get_row(bits):
                return combine_bits([get_bit(bits, i) for i in range(1, 6)])

            pattern = ((12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11),
                (10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8),
                (9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6),
                (4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13))

            return pattern[get_row(data)][get_no(data)]

        @staticmethod
        def S7(data):
            def get_bit(bits, i):
                return (bits & (1 << i)) >> (1 << i)

            def combine_bits(bits):
                combined = 0
                for (i, j) in zip(reversed(range(len(bits))), range(len(bits))):
                    combined |= bits[i] << j
                return combined

            def get_no(bits):
                return combine_bits([get_bit(bits, 0), get_bit(bits, 5)])

            def get_row(bits):
                return combine_bits([get_bit(bits, i) for i in range(1, 6)])

            pattern = ((4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1),
                (13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6),
                (1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2),
                (6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12))

            return pattern[get_row(data)][get_no(data)]

        @staticmethod
        def S8(data):
            def get_bit(bits, i):
                return (bits & (1 << i)) >> (1 << i)

            def combine_bits(bits):
                combined = 0
                for (i, j) in zip(reversed(range(len(bits))), range(len(bits))):
                    combined |= bits[i] << j
                return combined

            def get_no(bits):
                return combine_bits([get_bit(bits, 0), get_bit(bits, 5)])

            def get_row(bits):
                return combine_bits([get_bit(bits, i) for i in range(1, 6)])

            pattern = ((13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7),
                (1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2),
                (7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8),
                (2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11))

            return pattern[get_row(data)][get_no(data)]

    def __init__(self, key, message):
        self.key = key if type(key) is bytearray else bytearray(key)
        self.ciphertext = message if type(message) is bytearray else bytearray(message)

    def F(self, data, no):
        expanded = self.Transformation.E(data)

        key = self.KeySchedule.round_key(no, self.key)

        keyed = bytearray([d ^ k for (d, k) in zip(expanded, key)])

        substituted = self.Transformation.S(keyed)

        permuted = self.Transformation.P(substituted)

        return permuted

    def round(self, no):
        def divide():
            return (self.ciphertext[0:4], self.ciphertext[4:8])

        left, right = divide()
        left = bytearray([l ^ r for (l, r) in zip(left, self.F(right, no))])
        self.ciphertext = right + left
