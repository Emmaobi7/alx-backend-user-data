#!/usr/bin/env python3
"""
basic auth module
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """
    implement basic auth
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
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


    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
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
