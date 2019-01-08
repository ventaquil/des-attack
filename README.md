# Simple DES implementation in Python3

## Usage

Just import and use

    from des import Cipher as DES, random_key(), random_message()

    des = DES(random_key())
    ciphertext = des.encrypt(random_message())
    plaintext = des.decrypt(ciphertext)

## 6-rounds attack

Implemented 6-rounds differential attack allow to break 6 rounds of DES using differential cryptoanalisys.

Example code has been placed in `main.py` file under `break_6_rounds` function.

Output:

    Valid key: [4, 29, 11, 0, 43, 38, 50, 44] # key used by DES in 6th round
    Key candidate: [-1, 54, -1, -1, 43, 38, 50, 44] # potential keys (-1 inform that we cannot predict value)

## Tests

Use `pytest` to test prepared unit tests.

If you want to test your custom vectors you can use `openssl-test.sh` script.

Example:

    key=618A5B261AE3CD32
    plaintext=46112C8680041B44
    ./openssl-test.sh $key $plaintext
