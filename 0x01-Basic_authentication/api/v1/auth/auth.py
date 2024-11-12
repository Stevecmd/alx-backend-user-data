#!/usr/bin/env python3
""" Module of Authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Class to manage authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to check if authentication is required

        Args:
            path (str): the path to check
            excluded_paths (List[str]):
                     list of paths excluded from authentication

        Returns:
            bool: True if authentication is required, False otherwise
        """
        if path is None:
            # If path is None, authentication is required
            return True
        if excluded_paths is None or not excluded_paths:
            # If excluded_paths is empty or None, authentication is required
            return True
        # Ensure path ends with a slash for comparison
        if path[-1] != '/':
            path += '/'
        for excluded_path in excluded_paths:
            # Ensure excluded_path ends with asterisk for comparison
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            else:
                # Ensure excluded_path ends with a slash for comparison
                if excluded_path[-1] != '/':
                    excluded_path += '/'
                if path == excluded_path:
                    # If the path is in the excluded paths,
                    # authentication is not required
                    return False
        # If the path is not in the excluded paths, authentication is required
        return True

    def authorization_header(self, request=None) -> str:
        """
        Method to get the authorization header

        Args:
            request: the Flask request object

        Returns:
            str: the value of the Authorization header, or None
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method to get the current user """
        return None
