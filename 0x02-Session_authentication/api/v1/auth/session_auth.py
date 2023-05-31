#!/usr/bin/env python3
"""Session authentication"""
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """SessionAuth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates user session"""
        if user_id is None and not isinstance(user_id, str):
            return None

        s_id = str(uuid.uuid4())
        self.user_id_by_session_id[s_id] = user_id
        return s_id
