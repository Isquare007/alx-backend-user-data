#!/usr/bin/env python3
""" Flask view that handles all routes for the Session authentication
"""
from api.v1.views import app_views
from models.user import User
from flask import jsonify, abort, request, make_response
from os import getenv


@app_views.route("/auth_session/login", methods=['POST'], strict_slashes=False)
def handles_route():
    """handles all routes for the Session authentication"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or email == '':
        return jsonify({"error": "email missing"}), 400
    if not password or password == '':
        return jsonify({"error": "password missing"}), 400

    try:
        list_users = User.search({'email': email})
        user = list_users[0]
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    user_json = user.to_json()
    response = make_response(user_json)
    session_name = getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)

    return response


@app_views.route("/auth_session/logout",
                 methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """deletes a user's session at logout"""
    from api.v1.app import auth
    result = auth.destroy_session(request)
    if not result:
        abort(404)
    return jsonify({}), 200
