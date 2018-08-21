#!/usr/bin/python3
"""Users API routing"""

from models import storage
from flask import jsonify, request
from api.v1.views import app_views
from api.v1.app import not_found
from models.user import User


@app_views.route('/users/', methods=['GET'], strict_slashes=False)
def show_users():
    all_users = []
    users = list(storage.all('User').values())
    for user in users:
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>/', methods=['GET'], strict_slashes=False)
def display_user(user_id):
    user = storage.get("User", user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        return not_found(404)


@app_views.route('/users/<user_id>/', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    user = storage.get("User", user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({})
    else:
        return not_found(404)


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def create_user():
    error_message = ""
    content = request.get_json(silent=True)
    if isinstance(content, dict):
        if "email" not in content.keys():
            error_message = "Missing email"
        elif "password" not in content.keys():
            error_message = "Missing password"
        else:
            user = User(**content)
            storage.new(user)
            storage.save()
            response = jsonify(user.to_dict())
            response.status_code = 201
            return response
    else:
        error_message = "Not a JSON"
    response = jsonify({"error": error_message})
    response.status_code = 400
    return response


@app_views.route('/users/<user_id>/', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    ignore = ['id', 'email', 'created_at', 'updated_at']
    user = storage.get("User", user_id)
    if user:
        content = request.get_json(silent=True)
        if isinstance(content, dict):
            for key, value in content.items():
                if key not in ignore:
                    setattr(user, key, value)
            storage.save()
            return jsonify(user.to_dict())
        else:
            response = jsonify({"error": "Not a JSON"})
            response.status_code = 400
            return response
    else:
        return not_found(404)
