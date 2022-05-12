import sqlite3
from db import db

class UserModel(db.Model):
    # Telling SQLAlchemy about our db details where these models data will be stored
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    
    def __init__(self, _id, username, password):
        #Reason for _id is bcz id is a python keyword
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE Username = ?"
        row = cursor.execute(query, (username,)) #Always pass tuple and single value tuple=(x,)
        row_value = row.fetchone()
        if row_value:
            #user = cls(row_value[0], row_value[1], row_value[2]) or
            user = cls(*row_value)
        else:
            user = None

        connection.close()
        return user


    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE Id = ?"
        row = cursor.execute(query, (_id,)) #Always pass tuple and single value tuple=(x,)
        row_value = row.fetchone()
        if row_value:
            #user = cls(row_value[0], row_value[1], row_value[2]) or
            user = cls(*row_value)
        else:
            user = None

        connection.close()
        return user
