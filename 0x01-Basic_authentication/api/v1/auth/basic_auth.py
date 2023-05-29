#!/usr/bin/env python3
"""basic auth"""
from api.v1.auth.auth import Auth
import base64
# from typing import tuple


class BasicAuth(Auth):
    """basic authentication"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """extracts base authorization header"""
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """decodes base64"""
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_value = base64.b64decode(
                base64_authorization_header).decode('utf-8')
            return decoded_value
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header:
            str) -> tuple((str, str)):
        """extracts user email and password"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' in decoded_base64_authorization_header:
            email, password = decoded_base64_authorization_header.split(':')
            return email, password
        return None, None
