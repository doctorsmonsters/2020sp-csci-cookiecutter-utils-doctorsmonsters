from typing import Union
import hashlib
import os


def get_csci_salt() -> bytes:
    """Returns the appropriate salt for CSCI E-29

    :return: bytes representation of the CSCI salt
    """

    # Hint: use os.environment and bytes.fromhex
    salt = os.getenv("CSCI_SALT")
    return bytes.fromhex(salt)


def hash_str(some_val: Union[str, bytes], salt: Union[str, bytes] = "") -> bytes:
    """Converts strings to hash digest

    See: https://en.wikipedia.org/wiki/Salt_(cryptography)

    :param some_val: thing to hash, can be str or bytes
    :param salt: Add randomness to the hashing, can be str or bytes
    :return: sha256 hash digest of some_val with salt, type bytes
    """
    data_to_hash = str(salt) + some_val
    hash_object = hashlib.sha256(data_to_hash.encode())
    return hash_object.digest()


def get_user_id(username: str) -> str:
    salt = get_csci_salt()
    return hash_str(username.lower(), salt=salt).hex()[:8]
