#!/usr/bin/env python3
"""session expiration"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """deletes session after a duration"""

    def __init__(self) -> None:
        super().__init__()
        session_duration = getenv('SESSION_DURATION')
        try:
            self.session_duration = int(session_duration)
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """overload create session id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """overloads user_id_for session id"""
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        expire = created_at + timedelta(seconds=self.session_duration)
        if expire < datetime.now():
            return None

        return session_dict.get('user_id')
