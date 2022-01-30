from datetime import timedelta
import json
from flask import Flask, request
from flask.json import jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

import os

from resources.user import (
    UserRegister, 
    User, 
    UserLogin, 
    UserLogout,
    TokenRefresh
)

from resources.item import Item, Items
from resources.store import Store, Stores
from db import db
from blocklist import BLOCKLIST

app = Flask(__name__)
## Set JWT Secret Key
app.config['JWT_SECRET_KEY'] = "NikhilTopSecretKey654321"
app.secret_key = "nikhil"
api = Api(app)

## Set authentication url to /login (default is /auth)
app.config['JWT_AUTH_URL_RULE'] = '/login'

## Set to indicate where the DB is 
## os.getenv will default to sqlite if DATABASE_URL is not found
print (f"Getting DATABASE_URL from environment")
db_uri = os.getenv("DATABASE_URL", "sqlite:///data.db")
print (f"DATABASE_URL: {db_uri}")
## Fix the database url to have postgresql:// in case of postgres
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://")
    print (f"Updated database URL: {db_uri}")

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

## Disable Flask SQLAlchemy modifications tracker
## as SQLAlchemy does that automatically
app.config['SQLALCHECMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLOCKLIST_ENABLED'] = True
app.config['JWT_BLOCKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

## Initialise JWTManager
print ("Initialising JWT manager")
jwt = JWTManager(app)

## Decorator to load additional claims
@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    ## Check if user is having id = 1
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    print ("Checking is token is not in blocklist")
    print (f"JWT Headers: {jwt_header}")
    print (f"JWT Payload: {jwt_payload}")
    return jwt_payload['jti'] in BLOCKLIST

## Customise what we return when we get a request with
## expired token
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    print ("Got request with expired token")
    print (f"JWT Headers: {jwt_header}")
    print (f"JWT Payload: {jwt_payload}")
    return jsonify({
        'description': "The token has expired",
        'error': "token_expired"
    }), 401

## Customise what we return when we get some crap as 
## token
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def unauthorized_token_callback():
    return jsonify({
        'description': 'Request does not contain a valid token',
        'error': 'invalid_token'
    }), 401

@jwt.needs_fresh_token_loader
def need_fresh_token_callback(jwt_header, jwt_payload):
    print ("Got request where we need a fresh token but was not provided")
    print (f"JWT Headers: {jwt_header}")
    print (f"JWT Payload: {jwt_payload}")
    return jsonify({
        'description': 'This request needs a fresh token',
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'This token has been revoked. Please login again',
        'error': 'token_revoked'
    }), 401


## configure JWT token to expire after 30 mins
## this can be applied after creating JWT object
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

## Purely to understand the access token generated
## SHOULD NOT BE DONE generally
# @jwt.auth_response_handler
# def customized_response_handler(access_token, identity):
#     return jsonify({
#         'access_token': access_token.decode('utf-8'),
#         'user_id': identity.id
#     })

print ("Registering enpoint /item/<name>")
api.add_resource(Item, '/item/<string:name>')
print ("Registering enpoint /items")
api.add_resource(Items, '/items')
print ("Registering enpoint /store/<name>")
api.add_resource(Store, '/store/<string:name>')
print ("Registering enpoint /stores")
api.add_resource(Stores, '/stores')

print ("Registering enpoint /register")
api.add_resource(UserRegister, '/register')

print ("Registering enpoint /user")
api.add_resource(User, '/user/<int:user_id>')

print ("Registering endpoint /login")
api.add_resource(UserLogin, '/login')

print("Registering endpoint /refresh")
api.add_resource(TokenRefresh, '/refresh')

print("Registering endpoint /logout")
api.add_resource(UserLogout, '/logout')

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)