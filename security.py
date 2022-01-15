from werkzeug.security import safe_str_cmp
from models.user import UserModel

## Authenticate function that compares the users password
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    print (f"Attempting authenticating for User: {user.username}")
    ## use safe_str_cmp to automatically handle encodings
    ## and better comparisons
    if user and safe_str_cmp(user.password, password):
        ## password is matching, so return the user to generate JWT token
        print (f"User: {user.username} authenticated successfully")
        return user
    print (f"Authetication failed for User: {user.username}")

## Identity function checks if user id is valid
## Payload will contain the identity which will have user id
def identity(payload):
    # print(payload)
    user_id = payload["identity"]
    print (f"Request with JWT token having User id: {user_id}")
    return UserModel.find_by_id(user_id)