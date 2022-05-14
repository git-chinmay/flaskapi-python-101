from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT
from security import authentication, identity
from resources.user import UserRegistration
from resources.item import Item, ItemList
from resources.store import Store, StoreLists
import os


app = Flask(__name__)

# It will fetch DATABASE_URL value from Heroku, for local testing it will use sqlite
# Hence two parameters
# As Heroku dashboard not allowing the edit the conenction string we need to copy it to code and 
# modify the postgres:// into postgresql:// locally.
HEROKU_POSTGRE_DATABASE_URL = {"DATABASE_URL":"postgresql://uxxiqujuagnrsa:8075ab80c66bd7f88bd055cc3cf0bd691246439f88be2d90c32e2c8266cf06df@ec2-107-22-238-112.compute-1.amazonaws.com:5432/d2c7od2787c875"}
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///database.db') 
app.config['SQLALCHEMY_DATABASE_URI'] = HEROKU_POSTGRE_DATABASE_URL.get('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Will use this key to encrypt the data with JWT
# In production code we should store this key inside a vault like Hashicrop, Cyberark etc
app.secret_key = 'cicada'

api = Api(app)

#Creating a jwt object
jwt = JWT(app, authentication, identity) #/auth endpoint auto create


#Adding the resource to the api
api.add_resource(Item, '/item/<name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegistration, '/register')
api.add_resource(Store, '/store/<name>')
api.add_resource(StoreLists, '/stores')



if __name__ == "__main__":
    app.run(port=5000, debug=True)