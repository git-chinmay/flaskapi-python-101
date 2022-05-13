from regex import F
from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT
from security import authentication, identity
from resources.user import UserRegistration
from resources.item import Item, ItemList
from resources.store import Store, StoreLists


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
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