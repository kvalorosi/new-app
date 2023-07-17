from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

# from datetime import datetime


db = SQLAlchemy()


catch = db.Table(
    'catch',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True )
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
   
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)


    def save_user(self):
        db.session.add(self)
        db.session.commit()



class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    base_exp = db.Column(db.Integer, nullable=False)
    ability = db.Column(db.String, nullable=False)
    sprite = db.Column(db.String)
    caught = db.relationship('User',
            secondary = 'catch',
            backref = 'caught',
            lazy = 'dynamic'
            )

    
    
    def __init__(self, name=None, base_exp=None, ability=None, sprite=None):
        self.name = name
        self.base_exp = base_exp
        self.ability = ability
        self.sprite = sprite

    def save_pokemon(self):
        db.session.add(self)
        db.session.commit()

    
    def caught_poke(self, user):
        self.caught.append(user)
        db.session.commit()

    def release_poke(self, user):
        self.caught.remove(user)
        db.session.commit()


class Bikes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    pic = db.Column(db.String)


    def __init__(self, name, pic):
        self.name = name
        self.pic = pic

    def save_bikes(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'pic': self.pic
        }


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric(8,2))
    description = db.Column(db.String)
    image = db.Column(db.String)

    def __init__(self, title, price, description, image):
        self.title = title
        self. price = price
        self.description = description
        self.image = image

    def save_prod(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return{
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'description': self.description,
            'image': self.image
        }
     

    
    



    

