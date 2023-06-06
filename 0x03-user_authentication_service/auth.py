#!/usr/bin/env python3
"""auth module"""
import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """hash's a password with bcrypt"""

    bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()

    return bcrypt.hashpw(bytes, salt)


def _generate_uuid() -> str:
    """generates a new uuid"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a user"""
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hash_pass = _hash_password(password)
            new_user = self._db.add_user(email, hash_pass)
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """checks if the credentials is correct"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        password = password.encode('utf-8')
        if bcrypt.checkpw(password, user.hashed_password):
            return True

        return False
