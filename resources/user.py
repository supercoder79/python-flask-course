from werkzeug.security import safe_str_cmp
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username",
    type=str,
    required=True,
    help="username must be specified"
)
_user_parser.add_argument("password",
    type=str,
    required=True,
    help="password must be specified"
)

## Class to Register a new user
class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        print (f"Registering user {data.username}")

        ## Check if there is already as user with the same username
        if UserModel.find_by_username(data.username):
            return {'message': f"User with {data.username} already registered"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully!'}, 201

class User(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {"message": "User deleted"}, 200

class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get parser data
        data = _user_parser.parse_args()

        # find user in database
        user = UserModel.find_by_username(data['username'])

        # check password
        if user and safe_str_cmp(user.password, data['password']):
            # create access token
            access_token = create_access_token(identity=user.id, fresh=True)
            # create refresh token
            refresh_token = create_refresh_token(user.id)
            # return them
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        
        return {"message": "User does not exist"}, 400
        
        
        