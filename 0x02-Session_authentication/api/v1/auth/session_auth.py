#!/usr/bin/env python3
""" Module for Session Authentication
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """ Session Authentication Class """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id
        Args:
            user_id: user's identifier
        Returns:
            Session ID if user_id is valid, None otherwise
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns User ID based on Session ID
        Args:
            session_id: session identifier
        Returns:
            User ID if session_id is valid, None otherwise
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a User instance based on a cookie value
        Args:
            request: Flask request object
        Returns:
            User instance if found, None otherwise
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return None

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Deletes the user session / logs out
        Args:
            request: Flask request object
        Returns:
            True if the session was successfully destroyed, False otherwise
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        # Delete the Session ID from the user_id_by_session_id dictionary
        del self.user_id_by_session_id[session_id]
        return True
