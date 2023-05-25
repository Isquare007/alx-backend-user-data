#!/usr/bin/env python3
"""password hasher"""

import bcrypt


def hash_password(password: str) -> bytes:
    """return hashed password"""

    pass_bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(pass_bytes, salt)

    return hashed_password
