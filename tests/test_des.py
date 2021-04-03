from des import Cipher, function_s, KeyRandomGenerator, LinearTransformation, permutation, permutation_inverted, \
    PlaintextRandomGenerator, Sbox


def test_cipher():
    tuples = [("618A5B261AE3CD32", "46112C8680041B44", "060FBE89802B13AE"),
              ("C4F7A426A7D6430E", "771627F0C72351B4", "FB948449EA540995"),
              ("895D3E3885D3C289", "6916B343114A0876", "C3B914320945A917")]

    for key, plaintext, ciphertext in tuples:
        key = bytearray.fromhex(key)
        plaintext = bytearray.fromhex(plaintext)
        ciphertext = bytearray.fromhex(ciphertext)

        cipher = Cipher(key)
        assert key == cipher.key
        assert ciphertext == cipher.encrypt(plaintext)
        assert plaintext == cipher.decrypt(ciphertext)
        assert cipher.encrypt(plaintext) == cipher.encrypt(plaintext)
        assert cipher.decrypt(ciphertext) == cipher.decrypt(ciphertext)


def test_function_s():
    dataset = [[0x64, 0x79, 0x11, 0xCD, 0x7C, 0x74]]
    results = [[0x97, 0x44, 0xFE, 0x9A]]

    for data, expected in zip(dataset, results):
        data = bytearray(data)
        expected = bytearray(expected)
        assert expected == function_s(data)


def test_linear_transformation():
    pattern = (1, 2, 3, 4, 5, 6, 7, 8)
    lt0 = LinearTransformation(pattern)
    assert pattern == lt0.pattern

    dataset = [0xAB, 0xFC, 0x24, 0x5A, 0x67, 0x11]

    lt1 = LinearTransformation((1, 2, 3, 4, 5, 6, 7, 8))
    results = [0xAB, 0xFC, 0x24, 0x5A, 0x67, 0x11]
    for data, expected in zip(dataset, results):
        data = [data]
        data = bytearray(data)
        expected = [expected]
        expected = bytearray(expected)
        assert expected == lt1(data)

    lt2 = LinearTransformation((8, 7, 6, 5, 4, 3, 2, 1))
    results = [0xD5, 0x3F, 0x24, 0x5A, 0xE6, 0x88]
    for data, expected in zip(dataset, results):
        data = [data]
        data = bytearray(data)
        expected = [expected]
        expected = bytearray(expected)
        assert expected == lt2(data)

    lt3 = LinearTransformation((1, 1, 1, 1, 5, 5, 5, 5))
    results = [0xFF, 0xFF, 0x00, 0x0F, 0x00, 0x00]
    for data, expected in zip(dataset, results):
        data = [data]
        data = bytearray(data)
        expected = [expected]
        expected = bytearray(expected)
        assert expected == lt3(data)

    lt4 = LinearTransformation((1, 2, 3, 4, 5, 6, 7, 8, 5, 6, 7, 8, 1, 2, 3, 4))
    results = [[0xAB, 0xBA], [0xFC, 0xCF], [0x24, 0x42], [0x5A, 0xA5], [0x67, 0x76], [0x11, 0x11]]
    for data, expected in zip(dataset, results):
        data = [data]
        data = bytearray(data)
        expected = bytearray(expected)
        assert expected == lt4(data)


def test_key_random_generator():
    generator = KeyRandomGenerator()

    key = generator.generate()
    assert type(key) is bytearray
    assert len(key) * 8 == 64
    for byte in key:
        bits = 0
        for i in range(8):
            if (byte & (1 << i)) > 0:
                bits += 1
        assert 1 == (bits % 2)


def test_plaintext_random_generator():
    def test_plaintext(plaintext):
        assert type(plaintext) is bytearray
        assert len(plaintext) * 8 == 64

    generator = PlaintextRandomGenerator()

    plaintext = generator.generate()
    test_plaintext(plaintext)

    difference = bytearray([0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    plaintextes = generator.generate(difference)
    assert type(plaintextes) is tuple
    assert len(plaintextes) == 2
    for plaintext in plaintextes:
        test_plaintext(plaintext)
    assert difference == bytearray(p0 ^ p1 for p0, p1 in zip(plaintextes[0], plaintextes[1]))


def test_permutation_inverted():
    dataset = [[0x12, 0x34, 0x56, 0x78], [0xAB, 0xCD, 0xDC, 0xBA], [0x1D, 0xE2, 0x54, 0x16], [0x82, 0x32, 0xAF, 0x3B],
               [0x23, 0xD7, 0x10, 0xE0]]

    for data in dataset:
        data = bytearray(data)
        assert data == permutation_inverted(permutation(data))


def test_sbox():
    pattern = [[1, 2], [0, 3]]
    s0 = Sbox(pattern)
    assert pattern == s0.pattern

    s1 = Sbox([[0, 1], [3, 2]])
    assert 0 == s1(0, 0)
    assert 2 == s1(1, 1)

    s2 = Sbox([[1, 2, 0], [3, 0, 1]])
    assert 0 == s2(0, 2)
    assert 0 == s2(1, 1)
    assert 3 == s2(1, 0)
    assert 2 == s2(0, 1)
