#!/usr/bin/env python3
"""Session DB authentication module"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from models.base import Base
from datetime import datetime, timedelta
from typing import TypeVar


class SessionDBAuth(SessionExpAuth):
    """Session DB Authentication class"""

    def create_session(self, user_id=None):
        """Create and store new UserSession instance"""
        if user_id is None:
            return None

        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get User ID from session ID stored in DB"""
        if session_id is None:
            return None

        UserSession.load_from_file()
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return None

        user_session = sessions[0]

        # Fix: Check session expiration using created_at from user_session
        if self.session_duration <= 0:
            return user_session.user_id

        if not hasattr(user_session, 'created_at'):
            return None

        expired = self.session_duration and self.is_session_expired(
            user_session.created_at
        )
        if expired:
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroy UserSession based on Session ID from cookie"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        UserSession.load_from_file()
        sessions = UserSession.search({'session_id': session_id})
        if sessions:
            sessions[0].remove()
            return True

        return False

    def current_user(self, request=None) -> TypeVar('User'):
        """
            Returns the User instance based on the
            session ID from the request's cookie.

            Args:
                request: The Flask request object
                containing the session cookie.

            Returns:
                User instance if the session is valid
                and not expired, None otherwise.
        """
        session_id = self.session_cookie(request)
        user_session = UserSession.get(session_id)

        if not user_session:
            return None

        # Check if session has expired
        created_at = user_session.created_at
        session_duration = timedelta(seconds=self.session_duration)
        expiration_time = created_at + session_duration
        if datetime.utcnow() > expiration_time:
            return None

        return User.get(user_session.user_id)
