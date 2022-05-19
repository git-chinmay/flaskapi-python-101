from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask.json import jsonify
from blacklist import BLACKLIST

from db import db
from resources.user import UserRegister, User, UserLogin, RefreshToken, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'jose'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app) #It will not create /auth. We ahve to create it manually

#Adding JWT Claims
@jwt.additional_claims_loader
def add_claims_to_jwt(indentity):
    #The user with id=1 is admin
    if indentity == 1: #Insted of hardcoding we should get this vaue form database
        return {"is_admin":True}
    return {"is_admin":False}

# To check if token is blacklisted
# This identity we dont have to defined. Its coming from jwt inetrnal
# We are now checking jti of the user insted of id
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(decrypted_token):
    #return decrypted_token['identity'] in BLACKLIST
    return decrypted_token['jti'] in BLACKLIST

# When app received an expired token below function executed
@jwt.expired_token_loader
def expired_token_cllback(jwt_header, jwt_payload):
    return jsonify({
        "description":"The token has expired",
        "error":"token_expired"
    }), 401

# When app received the invalid token below function executed
@jwt.invalid_token_loader
def invalid_token_cllback(jwt_header, jwt_payload):
    return jsonify({
        "description":"Signature verification failed.",
        "error":"invalid_token"
    }), 401

# When app doen not receive a token from user below function executed
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description":"Request does not contain an access token.",
        "error":"authorised_required"
    }), 401

# When provided token is not a fresh one below function executed
@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return jsonify({
        "description":"Token is not fresh.",
        "error":"fresh_token_required"
    }), 401  

# When app needs to revoke the user due to unathorised token below function executed
@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "description":"The token has been revoked.",
        "error":"token_revoked"
    }), 401




api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(RefreshToken, '/refresh')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
