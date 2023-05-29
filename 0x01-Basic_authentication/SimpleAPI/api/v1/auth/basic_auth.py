#!/usr/bin/env python3

from .auth import Auth
import base64


class BasicAuth(Auth):
    """basic authentication"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """extracts base authorization header"""
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header.split(' ')[1]
        # encoded = base64.b64encode(author_header)
        # return encoded
