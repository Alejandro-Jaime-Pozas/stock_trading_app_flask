# create routes for the auth of users...
from . import bp as auth
from .http_auth import basic_auth, token_auth
from .models import User
from flask import jsonify, request


# create a user - longest code. need successful body: username, email, password, confirm pass
@auth.route('/users', methods=["GET", "POST"])
def create_user():
    data = request.json # this gets the input from the frontend fetch method body...
    # Validate the data
    for field in {'username', 'email', 'password'}:
        if field not in data:
            return jsonify({'error': f"You are missing the {field} field"}), 400
    # Grab the data from the request body
    username = data['username']
    email = data['email']
    # Check if the username or email already exists
    user_exists = User.query.filter((User.username == username)|(User.email == email)).all() # COME BACK, shouldn't this work with first()?
    # if it is, return back to signup
    if user_exists:
        return jsonify({'error': f"User with username {username} or email {email} already exists"}), 400
    # Create new user
    # new_user = User(username=username, email=email, password=data['password'])
    new_user = User(**data)

    return jsonify(new_user.to_dict())

# login - get token with username/password in header
@auth.route('/token', methods=["GET"])
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user() # this somehow retrieves the current user from db
    token = user.get_token()
    return jsonify({'token': token})

# update a user by id
@auth.route('/users/<int:id>', methods=["GET", "PUT"])
@token_auth.login_required
def updated_user(id):
    current_user = token_auth.current_user()
    if current_user.id != id:
        return jsonify({'error': 'You are not allowed to edit this user'}), 403 # what if no jsnofiy??
    user = User.query.get_or_404(id) # WHY GETTING THE USER AGAIN IF ALREADY HAVE USER IN current_user??
    data = request.json
    # if user tries to update username or email that other user has, reject
    for field in data:
        if field in ('username', 'email'):
            user_exists = User.query.filter((User.username == data[field])|(User.email == data[field])).first() # first should work here
            if user_exists:
                return jsonify({'error': f"{field}: {data[field]} already exists"}), 400 # bad request
    user.update(data)
    return jsonify(user.to_dict())


# delete a user by id
@auth.route('/users/<int:id>', methods=["GET", "DELETE"])
@token_auth.login_required
def delete_user(id):
    current_user = token_auth.current_user()
    if current_user.id != id:
        return jsonify({'error': 'You are not allowed to delete this user'}), 403
    user_to_delete = User.query.get_or_404(id)
    user_to_delete.delete()
    return jsonify({'success': f'{user_to_delete.username} has been deleted'})


# get user info from token
@auth.route('/me', methods=["GET"])
@token_auth.login_required
def me():
    return token_auth.current_user().to_dict() # grabs the current user if authenticated, and returns an object type...dk why no jsonify needed


# get all users - WILL NEED TO UPDATE THIS TO ONLY BE AVAILABLE FOR ADMIN USER, NOT TYPICAL USERS
@auth.route('/users', methods=["GET"])
@token_auth.login_required
def get_users():
    users = User.query.all() # this is a list...need to jsonify a list
    return jsonify([user.to_dict() for user in users])