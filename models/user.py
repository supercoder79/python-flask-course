from db import db

## Make the model import from SQLAlchemy
class UserModel(db.Model):
    ## Initialize __tablename__ variable to indicate to 
    ## SQLAlchemy which table it represents
    __tablename__ = 'users'

    ## table columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    ## Class method since it does not need to be executed
    ## on a user object. In fact it will be returning an
    ## user object
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        print (f"id = {_id}")
        return cls.query.filter_by(id=_id).first()