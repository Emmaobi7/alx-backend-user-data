#!/usr/bin/env python3
"""
session auth routes module
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth():
    """
    authenticate user and get session id
    """
    email = request.form.get('email')
    passwd = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    elif not passwd:
        return jsonify({"error": "password missing"}), 400
    data = User.search({'email': email})
    if not data:
        return jsonify({"error": "no user found for this email"}), 404

    if data:
        from api.v1.app import auth
        for user in data:
            if user.is_valid_password(passwd):
                session_id = auth.create_session(user.id)
                user_json = jsonify(user.to_json())
                user_json.set_cookie(getenv('SESSION_NAME'), session_id)
                return user_json
            else:
                return jsonify({"error": "wrong password"})


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    logout user
    """
    from api.v1.app import auth
    destroy_session = auth.destroy_session(request)
    if destroy_session is False:
        abort(404)
    else:
        return jsonify({}), 200
