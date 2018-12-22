#!/usr/bin/env bash
key=$1
plaintext=$2

printf $plaintext | \
    perl -e 'print pack "H*", <STDIN>' | \
    openssl enc -des-ecb -nopad -K $key -nosalt | \
    hexdump -C
