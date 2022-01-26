from flask_restful import Resource, reqparse
from models.user import UserModel

## Class to Register a new user
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
        type=str,
        required=True,
        help="username must be specified"
    )
    parser.add_argument("password",
        type=str,
        required=True,
        help="password must be specified"
    )
    
    def post(self):
        data = UserRegister.parser.parse_args()
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