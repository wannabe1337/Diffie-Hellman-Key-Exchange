# Ref.  https://en.wikipedia.org/wiki/HKDF#Example:_Python_implementation
#       https://datatracker.ietf.org/doc/html/rfc5869

import hashlib
import hmac
from math import ceil

hash_len = 32

def hmac_sha256(key, data):
    return hmac.new(key, data, hashlib.sha256).digest()

def hkdf(length: int, ikm, salt: bytes = b"", info: bytes = b"") -> bytes:
    """Key derivation function"""
    if len(salt) == 0:
        salt = bytes([0] * hash_len)
    prk = hmac_sha256(salt, ikm)
    t = b""
    okm = b""
    for i in range(ceil(length / hash_len)):
        t = hmac_sha256(prk, t + info + bytes([1 + i]))
        okm += t
    return okm[:length]