#from importlib.resources import Resource
import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

#WIll create a new resource for new user registration
class UserRegistration(Resource):

    parser = reqparse.RequestParser()    
    parser.add_argument(
        'username',
        type = str,
        required = True,
        help = "This field can not be left blank."
    )

    parser.add_argument(
        'password',
        type = str,
        required = True,
        help = "This field can not be left blank."
    )

    def post(self):

        data = UserRegistration.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message":f"User {data['username']} already exist."}, 400

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)" #Id coulmn will be null as its auto increment
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message" : f"User {data['username']} created successfully"}, 201
