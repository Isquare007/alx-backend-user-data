#!/usr/bin/env python3
"""auth module"""
import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


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

    def create_session(self, email: str) -> str:
        """creates a user session"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """gets user from user session passed"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
