# Simple DES implementation in Python

## Usage

Install by executing `python setup.py install` or `pip install .`.

Import like other package

```python
from des import Cipher as DES, random_key, random_message

des = DES(random_key())
message = random_message()
ciphertext = des.encrypt(message)
plaintext = des.decrypt(ciphertext)
print(plaintext == message)  # should be True
```

## 6-rounds attack

Implemented 6-rounds differential attack allow to break 6 rounds of DES using differential cryptoanalisys.

Example code has been placed in `des/main.py` file under `break_6_rounds` function.

```
$ python -m des
Encryption/decryption
difference  = 4008000004000000
plaintext   = EB47DCC8CF3D1DD7
plaintext'  = AB4FDCC8CB3D1DD7
key         = DC89256D162916DF
difference  = 0367457805008282 (same in 12%)
ciphertext  = FC9CE112286E9A23
ciphertext' = FFFBA46A2D6E18A1
ciphertext  = 0D6A0F43B0481DAA (final)
decrypted   = EB47DCC8CF3D1DD7 (valid)
6-round attack
Valid key: [57, 32, 42, 3, 38, 6, 15, 49]  # key used by DES in 6th round
Key candidate: [-1, 32, -1, -1, 0, 6, 15, 49]  # potential key (-1 inform that we cannot predict value)
Key candidate: [16, 0, -1, 3, 38, 6, -1, -1]  # potential key (-1 inform that we cannot predict value)
```

## Tests

Use `pytest` to run prepared unit tests.

```
$ pytest --verbose tests/
===================================================================================================== test session starts =====================================================================================================
platform linux -- Python 3.9.0+, pytest-6.2.2, py-1.10.0, pluggy-0.13.1 -- /home/user/des-attack/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/user/des-attack
collected 7 items

tests/test_des.py::test_cipher PASSED                                                                                                                                                                                   [ 14%]
tests/test_des.py::test_function_s PASSED                                                                                                                                                                               [ 28%]
tests/test_des.py::test_linear_transformation PASSED                                                                                                                                                                    [ 42%]
tests/test_des.py::test_key_random_generator PASSED                                                                                                                                                                     [ 57%]
tests/test_des.py::test_plaintext_random_generator PASSED                                                                                                                                                               [ 71%]
tests/test_des.py::test_permutation_inverted PASSED                                                                                                                                                                     [ 85%]
tests/test_des.py::test_sbox PASSED                                                                                                                                                                                     [100%]

====================================================================================================== 7 passed in 0.20s ======================================================================================================
```
