from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
_user_parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )


class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        return {"message":"User not found."}, 404

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return {"message":"User deleted."}, 200
        return {"message":"User not found."}, 404


class UserLogin(Resource):

    @classmethod
    def post(cls):
        # Get the username from parser
        data = _user_parser.parse_args()

        # find the user in database
        user = UserModel.find_by_username(data['username'])

        # Check password
        if user and safe_str_cmp(user.password, data['password']):
            # Crate an auth token
            access_token = create_access_token(identity=user.id, fresh=True)

            # Create a refresh token
            refresh_token = create_refresh_token(identity=user.id)

            return {
                "access_token" : access_token,
                "refresh_token" : refresh_token
            }, 200

        return {"message":"Invalid credential."}, 401
        
        