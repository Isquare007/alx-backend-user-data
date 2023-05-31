#!/usr/bin/env python3
"""Auth class
"""
from flask import request
from os import getenv
from typing import List, TypeVar


class Auth:
    """a class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth method"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        if path.endswith('/'):
            path = path[:-1]

        for excluded_path in excluded_paths:
            if path == excluded_path.rstrip('/'):
                return False
            if excluded_path.endswith(
                    '*') and path.startswith(excluded_path.rstrip('*')):
                return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Unauthorization header"""
        if request is None:
            return None
        authorization_header = request.headers.get('Authorization')

        if authorization_header is None:
            return None

        return authorization_header

    def current_user(self, request=None) -> TypeVar('User'):
        """return the current user"""
        return None

    def session_cookie(self, request=None):
        """returns session cookie"""
        if request is None:
            return None
        SESSION_NAME = getenv('SESSION_NAME')
        return request.cookies.get(SESSION_NAME)
