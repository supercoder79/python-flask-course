from app import app
from db import db

db.init_app(app)

## Flask decorator to indicate method should run before first request
@app.before_first_request
def create_tables():
    ## It will create if not present the tables in the DB
    print ("Creating tables in database")
    db.create_all()

