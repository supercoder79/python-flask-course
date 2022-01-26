from db import db

## Inherit the ItemModel class from SQLAlchemy.Model
class ItemModel(db.Model):
    ## Set __tablename__ variable to the DB table
    ## for this model
    __tablename__ = 'items'

    ## Define the columns in the 'item' table
    ## names of the column variables should match
    ## the names of the Model class
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    ## foreign key for stores table
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    ## establish a join
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'store_id': self.store_id
        }
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1
    
    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db (self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()