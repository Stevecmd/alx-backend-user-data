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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that the provided password matches the hashed password
    Args:
        hashed_password: The hashed password
        password: The password to validate
    Returns:
        True if the password matches the hash, False otherwise
    """
    # Convert the password string to bytes
    password_bytes = password.encode('utf-8')

    # Check if the password matches the hash
    return bcrypt.checkpw(password_bytes, hashed_password)
