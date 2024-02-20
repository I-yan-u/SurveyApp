from flask import Flask, jsonify, make_response, abort, request
from api.v1.auth.auth import BasicAuth, JWTAuth, token_required, Auth
from api.v1.views import app_view
from models import store
from models.user import User
from datetime import datetime, timedelta

auth = Auth()
bAuth = BasicAuth()
jAuth = JWTAuth()


@token_required
def user_data(user):
    if user:
        return user
    return None


@app_view.route('/login', methods=['GET'], strict_slashes=False)
def user_login():
    validate = bAuth.validate(request)
    if validate:
        user = bAuth.current_user(request)
        payload = {
            'email': user.email,
            'id': user.id,
            'creator': user.creator,
            'exp': datetime.utcnow() + timedelta(minutes=60)
        }
        token = jAuth.encode_token(payload)
        return jsonify({'token': token, 'id': user.id})
    return make_response(jsonify({'message': 'Login Failed'}), 401)

    
@app_view.route('/user/<uid>', methods=['GET'], strict_slashes=False)
@token_required
def get_user(user, uid):
    if user and user.id == uid:
        return make_response(jsonify(user.to_dict()), 200)
    else:
        return make_response(jsonify({'error': 'Unauthorised'}), 401)
    

@app_view.route('/create_user', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new user"""
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in data:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in data:
        return make_response(jsonify({"error": "Missing password"}), 400)
    if 'first_name' not in data:
        return make_response(jsonify({"error": "Missing First name"}), 400)
    if 'last_name' not in data:
        return make_response(jsonify({"error": "Missing Last name"}), 400)
    if 'creator' not in data:
        data['creator'] = False
    elif 'creator' in data:
        if data.get('creator') == 'True' or data.get('creator') == 'true':
            data['creator'] = True
        else:
            data['creator'] = False
    try:
        new_user = auth.register_user(**data)
        return make_response(jsonify(new_user.to_dict()), 201)
    except ValueError:
        return make_response(jsonify({'message': 'User Already exsit'}), 403)
    
@app_view.route('/update_user', methods=['PUT'], strict_slashes=False)
@token_required
def update_user(user):
    data = request.get_json()
    for k, v in data.items():
        if k == 'creator':
            if v == 'True' or v == 1 or v == 'true':
                v = True
            else:
                v = False
        if hasattr(user, k):
            setattr(user, k, v)
    user.save()
    return make_response(jsonify({'message': 'User updated'}), 201)
