#!/usr/bin/env python3
"""SessionDBAuth"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """stores session_id in a DB"""

    def create_session(self, user_id=None):
        """overloads create session"""
        user_session = super().create_session(user_id)
        return user_session

    def user_id_for_session_id(self, session_id=None):
        """overloads user id for session"""
        if session_id is None:
            return None

        UserSession.load_from_file

        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return None

        user_session = user_session[0]
        expire = user_session.created_at + \
            timedelta(seconds=self.session_duration)
        if expire < datetime.now():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """destrolys user session"""
        if request is None:
            return False

        session_id = self.session_cookie(request)

        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return False

        user_session = UserSession.search({'session_id': session_id})

        if not user_session:
            return False

        user_session = user_session[0]

        try:
            user_session.remove()
            UserSession.save_to_file
        except Exception:
            return False

        return True
