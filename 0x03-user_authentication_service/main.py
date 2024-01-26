#!/usr/bin/env python3
"""
tests routes module
"""

import requests
BASE_URL = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """
    tests endpoint
    """
    data = {"email": email, "password": password}
    resp = requests.post(f'{BASE_URL}/users', data=data)
    assert resp.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """
    test login wrong password
    """
    data = {"email": email, "password": password}
    resp = requests.post(f'{BASE_URL}/sessions', data=data)
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    test log in route
    """
    data = {"email": email, "password": password}
    resp = requests.post(f'{BASE_URL}/sessions', data=data)
    assert resp.status_code == 200
    session_id = resp.cookies.get('seesion_id')
    return session_id


def profile_unlogged() -> None:
    """
    test no logged in profile
    """
    resp = requests.get(f'{BASE_URL}/profile')
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    test log in profile
    """
    data = {"session_id": session_id}
    resp = requests.get(f'{BASE_URL}/profile', cookies=data)
    assert resp.status_code == 200


def log_out(session_id: str) -> None:
    """
    test logout route
    """
    data = {"session_id": session_id}
    resp = requests.delete(f'{BASE_URL}/sessions', cookies=data)
    assert resp.status_code == 200


def reset_password_token(email: str) -> str:
    """
    test password reset
    """
    data = {"email":  email}
    resp = requests.post(f'{BASE_URL}/reset_password', data=data)
    assert resp.status_code == 200
    reset_token = resp.json().get('reset_token')
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    update password test
    """
    data = {"email": email,
            "reset_token": reset_token,
            "new_password": new_password
            }
    resp = requests.put(f'{BASE_URL}/reset_password', data=data)
    assert resp.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
