""" controllers """
from flask import current_app as app, request
from marshmallow import ValidationError
from alch.db import Session as db
from alch.models import User
from alch.schema import user_sch, users_sch


@app.route('/')
def home():
    """ get all users """
    users = db.query(User).all()

    return {'users': users_sch.dump(users)}


@app.route('/user/<int:uid>')
def get_user(uid):
    """ get single user"""
    if (user := db.query(User).get(uid)) is None:
        return {'msg': 'user does not exist'}, 422

    return {'user': user_sch.dump(user)}


@app.route('/user', methods=['POST'])
def insert_user():
    """ inser a new user """
    body = request.get_json()
    if not body:
        return {'msg': 'no input data provided'}, 400

    # validate and deserialize
    try:
        sch = user_sch.load(body)
    except ValidationError as err:
        return err.messages, 422

    # persist
    user = User(name=sch['name'])
    db.add(user)
    db.commit()

    return {'user': user_sch.dump(user)}


@app.route('/user/<int:uid>', methods=['PUT'])
def update_user(uid):
    """ update an existing user """
    body = request.get_json()
    if not body:
        return {'msg': 'no input data provided'}, 400

    # validate and deserialize
    try:
        sch = user_sch.load(body)
    except ValidationError as err:
        return err.messages, 422

    # find
    if (user := db.query(User).get(uid)) is None:
        return {'msg': 'user does not exist'}, 422

    # persist
    user.name = sch['name']
    db.commit()

    return {'user': user_sch.dump(user)}
