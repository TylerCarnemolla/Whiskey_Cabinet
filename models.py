from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func 

import uuid
from datetime import datetime
from marshmallow import Schema, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets
ma = Marshmallow()
db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key = True, unique=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default= '')
    g_auth_verify = db.Column (db.Boolean, default = False)
    token = db.Column(db.String, default='', unique = True)
    date_created = db.Column(db.DateTime, nullable=False, server_default=func.now())




    def __init__(self, email, first_name='', last_name='',password='', token='', g_auth_verify=False ):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    
    def set_token(self, length):
        return secrets.token_hex(length)   
        
    def set_id(self):
        return secrets.token_urlsafe()
        return str(uuid.uuid4()) 
        
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
        
    def __repr__ (self):
        return f"User {self.email} has been added to the database."
        

       
class Whiskey(db.Model):
    id=db.Column(db.String, primary_key = True)
    brand = db.Column(db.String(150), nullable = False) 
    kind = db.Column(db.String(150))
    proof = db.Column(db.String(10))
    notes = db.Column(db.String(200))
    origin = db.Column(db.String(50))
    user_token = db.Column(db.String, db.ForeignKey( 'user.token'), nullable = False)

    def __init__ ( self, brand , kind, proof, notes, origin, user_token, id=''):
        self.id = self.set_id()
        self.brand = brand
        self.kind = kind 
        self.proof = proof
        self.notes = notes
        self.origin = origin
        self.user_token = user_token

    def __repr__(self):
        return f'The following whyskey has been added to your shelf: {self.brand}'
        
    def set_id(self):
        return secrets.token_urlsafe()
        
class BoozeSchema(ma.Schema): 
    class Meta:
        fields = ['id', 'brand', 'kind', 'proof', 'notes', 'origin']

booze_schema = BoozeSchema()
bottles_schema = BoozeSchema(many=True)

