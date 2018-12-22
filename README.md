# Simple DES implementation in Python3

## Usage

Just import and use

    from des import Cipher as DES, random_key(), random_message()

    des = DES(random_key())
    ciphertext = des.encrypt(random_message())
    plaintext = des.decrypt(ciphertext)

## Tests

Use `pytest` to test prepared unit tests.

If you want to test your custom vectors you can use `openssl-test.sh` script.

Example:

    key=618A5B261AE3CD32
    plaintext=46112C8680041B44
    ./openssl-test.sh $key $plaintext
