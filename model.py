from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    email = db.Column(db.String(150), primary_key = True)
    image = db.Column(db.String(500))
    token = db.Column(db.Integer)