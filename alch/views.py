""" controllers """
from flask import current_app as app, request
from marshmallow import ValidationError
from alch.db import Session as db
from alch.models import User
from alch.schema import user_sch, users_sch
from alch.redis_cache import Client as red


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


@app.route('/redis/w')
def redis_write():
    """Write to redis, strings and hashes."""
    ok = red.set('sample:firstkey', 'some data here')

    second = {
        'id': 6,
        'name': 'myname',
        'email': 'myname2@hs.ae'
    }
    ok2 = red.hset('user:{}'.format(second['id']), mapping=second)

    return {'set': ok, 'hset': ok2}


@app.route('/redis/r')
def redis_read():
    """Read from redis, strings and hashes."""
    val = red.get('sample:firstkey')

    val2 = red.hgetall('user:{}'.format(6))

    val3 = red.hget('user:{}'.format(6), 'email')

    return {'get': val, 'hgetall': val2, 'hget': val3}
