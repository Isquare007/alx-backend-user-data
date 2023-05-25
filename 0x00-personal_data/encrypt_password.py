#!/usr/bin/env python3
"""password hasher"""

import bcrypt


def hash_password(password: str) -> bytes:
    """return hashed password"""

    pass_bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(pass_bytes, salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """check if password is valid"""
    pass_bytes = password.encode('utf-8')

    return bcrypt.checkpw(pass_bytes, hashed_password)
