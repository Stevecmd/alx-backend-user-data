#!/usr/bin/env python3
""" Module for Basic Authentication
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """
    Class to manage basic authentication
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header
        for Basic Authentication

        Args:
            authorization_header (str): The Authorization header

        Returns:
            str: The Base64 part of the Authorization header, or None
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 part of the Authorization header.

        Args:
            base64_authorization_header (str):
                                        Base64 encoded Authorization header.

        Returns:
            str: Decoded value of the Base64 string, or None if decoding fails.

        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None
