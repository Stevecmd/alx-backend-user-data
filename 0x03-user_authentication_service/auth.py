#!/usr/bin/env python3
"""Auth module
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """
    Generates a new UUID.

    Returns:
        str: The string representation of the UUID.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user.

        Args:
            email (str): The email address of the user.
            password (str): The password of the user.

        Raises:
            ValueError: If the email is already registered.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates user login.

        Args:
            email (str): The email address of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            is_valid_password = bcrypt.checkpw(
                password.encode('utf-8'), user.hashed_password
            )
            return is_valid_password
        except NoResultFound:
            return False
