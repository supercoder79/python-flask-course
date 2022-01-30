from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, 
    get_jwt, 
    get_jwt_identity
)

from models.item import ItemModel

## Define Resource for items
class Items(Resource):
    ## GET /items 
    ## returns all items
    ## User login is optional, if logged-in you get all info
    @jwt_required(optional=True)
    def get(self):
        ## Get user_id of user if logged in
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        ## Check if user is logged-in, then return all details
        ## else return only item names
        if user_id:
            # print (f"Get /items called by a logged-in user")
            ## using list comprehension
            ## more 'pythonic' and readable :)
            return {'items': items}, 200
        # print ("User is not logged-in. Returning limited information")
        return {
            'items': [item['name'] for item in items],
            'message': "Nore data available if you log in"
        }, 200
        
        ## using lambda functions & map
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}, 200


## Define resource for item
class Item(Resource):
    ## Parser for parsing POST/PUT requests to ensure
    ## they have the correct JSON payload 
    parser = reqparse.RequestParser()
    ## 'price'
    parser.add_argument('price',
        type=float,
        required=True,
        help="Price cannot be blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )

    ## @jwt_required - decorator indicates the API has to have
    ## Authorization Header with valid JWT token
    @jwt_required()
    def get(self, name):
        # # filter(function to filter on)
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # return {"item": item}, 200 if item else 404
        
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found'}, 404

    ## Require a fresh JWT access token
    @jwt_required(fresh=True)   
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name {name} already exists"}, 400
        
        request_data = Item.parser.parse_args()
        ## or user **request_data for dictionary unpacking
        item = ItemModel(name, **request_data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occured during inserting the item"}, 500
        
        return item.json(), 201
    
    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        print (f"JWT claims: {claims}")
        ## Check claims if 'is_admin' is 1
        if not claims['is_admin']:
            return {"message": "Admin privilege required"}, 401
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return {"message": "Item deleted"}
    
    def put (self, name):
        request_data = Item.parser.parse_args()

        # item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = Item(name, **request_data)
        else:
            item.price = request_data['price']
            item.store_id = request_data['store_id']

        item.save_to_db()
        return item.json()
