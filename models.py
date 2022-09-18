from datetime import datetime
from app import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Your database models should go here.
# Check out the Flask-SQLAlchemy quickstart for some good docs!
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/


class Club(db.Model):
    code = db.Column(db.String(20), unique=True, nullable=False, primary_key = True)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    tags = db.Column(db.Text())
    favorites = db.Column(db.Integer(), default = 0)

    def to_dict(self):
        return {'code': self.code,
        'name': self.name,
        'description': self.description,
        'tags': self.tags,
        'favorites': self.favorites}

class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key = True, unique = True)
    username = db.Column(db.Text, unique=True, primary_key = True)
    name = db.Column(db.String(40), nullable=False)
    grad = db.Column(db.Integer())
    major = db.Column(db.String(50))
    hash = db.Column(db.Text())
    salt = db.Column(db.String(60))
    email = db.Column(db.String(50), unique = True)
    # lastlogin = db.Column(db.Time(), default = datetime.now)
    favorites = db.Column(db.Text())

    # is_authenticated = db.Column(db.Boolean(), default = False)
    # auth_ip = db.Column(db.String(20), default = "0.0.0.0")

    def to_dict(self):
        return {'name': self.name,
                'grad': self.grad,
                'major': self.major}
