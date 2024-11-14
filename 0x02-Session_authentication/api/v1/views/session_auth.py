#!/usr/bin/env python3
""" Module for Session Authentication views
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """ POST /auth_session/login
    Handles user login and creates a session.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or email == '':
        return jsonify({"error": "email missing"}), 400

    if not password or password == '':
        return jsonify({"error": "password missing"}), 400

    # Retrieve the User instance based on the email
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a Session ID for the User ID
    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    if not session_id:
        return jsonify({"error": "can't create session"}), 500

    user_json = user.to_json()
    response = jsonify(user_json)
    session_name = getenv("SESSION_NAME")
    if not session_name:
        # Default session name if environment variable is not set
        session_name = "_my_session_id"
    response.set_cookie(session_name, session_id)

    return response


@app_views.route(
    '/auth_session/logout',
    methods=['DELETE'],
    strict_slashes=False
)
def auth_session_logout():
    """ DELETE /auth_session/logout
    Handles logging out and destroying the session.
    """
    # Import inside the function to avoid circular import
    from api.v1.app import auth

    destroyed = auth.destroy_session(request)
    if not destroyed:
        abort(404)

    return jsonify({}), 200
