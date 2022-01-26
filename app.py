from datetime import timedelta
from flask import Flask, request
from flask.json import jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

import os

from resources.user import UserRegister, User, UserLogin
from resources.item import Item, Items
from resources.store import Store, Stores
from db import db

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

## Initialise JWTManager
print ("Initialising JWT manager")
jwt = JWTManager(app)

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}


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

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)