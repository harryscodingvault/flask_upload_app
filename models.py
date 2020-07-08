from app import db, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(50))
class Album(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    photos = db.relationship('Photo', backref='album', lazy='dynamic') 
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    image = db.Column(db.String(100))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))