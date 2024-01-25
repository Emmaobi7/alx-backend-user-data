#!/usr/bin/env python3
"""
Auth module
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth():
    """
    api authentication class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        return: true or false
        """
        if path is None or excluded_paths is None or not len(excluded_paths):
            return True
        if path[-1] != '/':
            path += '/'
        if excluded_paths[-1] != '/':
            excluded_paths += '/'
        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        authorize all requests
        return: None or header request
        """
        if request is None:
            return None
        if not request.headers.get("Authorization"):
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        return: none
        """
        return None

    def session_cookie(self, request=None):
        """
        return: cookie from a request
        """
        if request is None:
            return None
        session_name = getenv('SESSION_NAME')
        return request.cookies.get(session_name)
