import json
import os
from app import db, DB_FILE
import bcrypt
from datetime import datetime

def create_user():
    salt = bcrypt.gensalt()
    josh = User(id = 31394502,
    username = "josh",
    name = "Josh Doe",
    grad = 2026,
    major = "Computer Science",
    hash = bcrypt.hashpw(b"password", salt),
    salt = salt,
    favorites = json.dumps([]),
    email = "joshdoe@upenn.edu")
    
    db.session.add(josh)
    db.session.commit()
from models import *

def load_data():
    file = open("clubs.json")
    data = json.load(file)
    for i in data:
        club = Club(code = i["code"],
        name = i["name"],
        description = i["description"],
        tags =  json.dumps(i["tags"]))
        print(club.name)
        db.session.add(club)       
    db.session.commit()



# No need to modify the below code.
if __name__ == '__main__':
    # Delete any existing database before bootstrapping a new one.
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    db.create_all()
    create_user()
    load_data()
