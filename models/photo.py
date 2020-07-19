from db import db


class PhotoModel(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    url = db.Column(db.String(80))

    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
    album = db.relationship('AlbumModel')

    def __init__(self, name, url, album_id):
        self.name = name
        self.url = url
        self.album_id = album_id

    def json(self):
        return {'name': self.name, 'url': self.url}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()