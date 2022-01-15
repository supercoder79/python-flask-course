from db import db

## Inherit the ItemModel class from SQLAlchemy.Model
class StoreModel(db.Model):
    ## Set __tablename__ variable to the DB table
    ## for this model
    __tablename__ = 'stores'

    ## Define the columns in the 'item' table
    ## names of the column variables should match
    ## the names of the Model class
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for  item in self.items.all()]}
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1
    
    def save_to_db (self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()