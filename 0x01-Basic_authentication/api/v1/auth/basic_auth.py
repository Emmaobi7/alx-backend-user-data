#!/usr/bin/env python3
"""
basic auth module
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    implement basic auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        return: base64 of auth header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        base64 = authorization_header.split(' ')
        return base64[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        decode base64 header string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            base64encode = base64_authorization_header.encode('utf-8')
            base64decode = base64.b64decode(base64encode)
            decodedval = base64decode.decode('utf-8')
            return decodedval
        except Exception as e:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        get user credentials
        username(str)
        password(str)
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_info = decoded_base64_authorization_header.split(':', 1)
        return user_info[0], user_info[1]

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """
        user object
        return: user instance if in DB
        """
        if not isinstance(user_email, str) or user_email is None:
            return None
        if not isinstance(user_pwd, str) or user_pwd is None:
            return None
        try:
            users = User.search({'email': user_email})
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception as e:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overload auth
        retrieve user instance for a requests
        """
        try:
            header = seld.authorization_header(request)
            base64header = self.extract_base64_authorization_header(header)
            decodeval = self.decode_base64_authorization_header(base64header)
            user_inf = self.extract_user_credentials(decodeval)
            user = self.user_object_from_credentials(user_inf[0], user_inf[1])
            return user
        except Exception as e:
            return None
