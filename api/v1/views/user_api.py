from flask import Flask, jsonify, make_response, abort, request
from api.v1.views import app_view
from models import store
from models.user import User
from web_app.auth import Auth

auth = Auth()


def user_data():
    session_id = request.cookies.get('session_id')
    user = auth.get_user_from_session(session_id)
    if user:
        return user
    return None


@app_view.route('/login', methods=['POST'], strict_slashes=False)
def user_login():
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Invalid data type"}), 400)
    # print(data)
    if 'email' not in data:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in data:
        return make_response(jsonify({"error": "Missing password"}), 400)

    email = data.get('email')
    password = data.get('password')
    validate = auth.valid_login(email, password)
    if validate:
        session_id = auth.create_session(email)
        response = make_response(jsonify(session_id), 201)
        response.set_cookie('session_id', session_id)
        return response
    else:
        return make_response(jsonify({'error': 'Invalid email or password'}), 401)
    

@app_view.route('/user/<uid>', methods=['GET'], strict_slashes=False)
def get_user(uid):
    user = user_data()
    if user and user.id == uid:
        return make_response(jsonify(user.to_dict()), 200)
    else:
        return make_response(jsonify({'error': 'Unauthorised'}), 401)
    

# @app_view.route('/users', methods=['POST'], strict_slashes=False)
# def create_user():
#     """Create a new user"""
#     data = request.get_json()
#     if not data:
#         return make_response(jsonify({"error": "Not a JSON"}), 400)
#     if 'email' not in data:
#         return make_response(jsonify({"error": "Missing email"}), 400)
#     if 'password' not in data:
#         return make_response(jsonify({"error": "Missing password"}), 400)
#     if 'first_name' not in data:
#         return make_response(jsonify({"error": "Missing First name"}), 400)
#     if 'last_name' not in data:
#         return make_response(jsonify({"error": "Missing Last name"}), 400)
#     new_user = User(**data)
#     store.new(new_user)
#     store.save()
#     return make_response(jsonify(new_user.to_dict()), 201)