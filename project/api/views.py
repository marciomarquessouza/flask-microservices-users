#project/api/views.py

from flask              import Blueprint, jsonify,request
from project.api.models import User
from project            import db
from sqlalchemy         import exc

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

    if not post_data :
        response_object = {
            'status' : 'fail',
            'message' : 'Invalid payload.'
        }
        return jsonify(response_object),400

    username = post_data.get('username')
    email = post_data.get('email')

    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            #Recording the data received in the db
            db.session.add(User(username=username,email=email))
            db.session.commit()
            #Sending a success response
            response_object = {
                'status': 'success',
                'message': f'{email} was added!'
            }
            return jsonify(response_object),201
        else:
            response_object = {
                'status' : 'fail',
                'message' : 'Sorry. That email already exists.'
            }
            return jsonify(response_object),400
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status' : 'fail',
            'message' : 'Invalid payload.'
        }
        return jsonify(response_object),400

@users_blueprint.route('/users/<user_id>',methods=['GET'])
def get_single_user(user_id):
    """ Get a single user details """
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            response_object = {
                'status':'fail',
                'message':'User does not exist'
            }
            return jsonify(response_object),404
        else:
            response_object = {
                'status' : 'success',
                'data': {
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.created_at
                }
            }
            return jsonify(response_object),200
    except ValueError:
        response_object = {
            'status':'fail',
            'message':'User format is not valid'
        }
        return jsonify(response_object),404
