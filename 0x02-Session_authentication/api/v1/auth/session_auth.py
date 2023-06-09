#!/usr/bin/env python3
"""Session authentication"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """SessionAuth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates user session"""
        if user_id is None or not isinstance(user_id, str):
            return None

        s_id = str(uuid.uuid4())
        self.user_id_by_session_id[s_id] = user_id
        return s_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns the user id based on the user session id"""
        if session_id is None and not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """overload that returns a user"""
        if request is None:
            return
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user = self.user_id_for_session_id(session_id)
        return User.get(user)

    def destroy_session(self, request=None):
        """deletes user session on logout"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        try:
            del self.user_id_by_session_id[session_id]
        except Exception:
            pass

        return True
