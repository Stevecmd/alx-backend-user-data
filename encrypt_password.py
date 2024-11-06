#!/usr/bin/env python3
"""
Password encryption module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt
    Args:
        password: The password to hash
    Returns:
        A salted, hashed password as a byte string
    """
    # Convert the password string to bytes
    password_bytes = password.encode('utf-8')

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)

    return hashed
