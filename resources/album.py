from flask_restful import Resource
from models.album import AlbumModel


class Album(Resource):
    def get(self, name):
        album = AlbumModel.find_by_name(name)
        if album:
            return album.json()
        return {'message': 'Album not found'}, 404

    def post(self, name):
        if AlbumModel.find_by_name(name):
            return {'message': "An album with name '{}' already exists.".format(name)}, 400

        album = AlbumModel(name)
        try:
            album.save_to_db()
        except:
            return {"message": "An error occurred creating the album."}, 500

        return album.json(), 201

    def delete(self, name):
        album = AlbumModel.find_by_name(name)
        if album:
            album.delete_from_db()

        return {'message': 'Album deleted'}


class AlbumList(Resource):
    def get(self):
        return {'album': list(map(lambda x: x.json(), AlbumModel.query.all()))}