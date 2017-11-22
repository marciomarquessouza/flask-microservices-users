#project/api/views.py

from flask import Blueprint, jsonify,request
from project.api.models import User
from project import db

users_blueprint = Blueprint('users',__name__)

@users_blueprint.route('/ping',methods=['GET'])
def ping_pong():
    return jsonify( {
        'status': 'success',
        'message': 'pong!'
    })

@users_blueprint.route('/users',methods=['POST'])
def add_user():
    #Recovering the request data
    post_data = request.get_json()
    username = post_data.get('username')
    email = post_data.get('email')

    #Recording the data received in the db
    db.session.add(User(username=username,email=email))
    db.session.commit()

    #Sending a success response
    response_object = {
        'status': 'success',
        'message': f'{email} was added!'
    }

    return jsonify(response_object),201
