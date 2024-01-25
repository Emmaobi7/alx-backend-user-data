#!/usr/bin/env python3
"""
session authentiocation module
"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """
    implement session authenktication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        create session id for a user_id
        return(str): session id
        """
        if not isinstance(user_id, str) or user_id is None:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        return(str): user id based on session id
        """
        if not isinstance(session_id, str) or session_id is None:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        return: user instance based on cookie value
        """
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return None
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        destroy active user session
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        del self.user_id_by_session_id[session_id]
        return True
