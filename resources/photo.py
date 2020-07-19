from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.photo import PhotoModel


class Photo(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('url',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('album_id',
                        type=int,
                        required=True,
                        help="Every item needs a album_id."
                        )

    @jwt_required()
    def get(self, name):
        photo = PhotoModel.find_by_name(name)
        if photo:
            return photo.json()
        return {'message': 'Photo not found'}, 404

    def post(self, name):
        if PhotoModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Photo.parser.parse_args()

        photo = PhotoModel(name, **data)

        try:
            photo.save_to_db()
        except:
            return {"message": "An error occurred inserting the photo."}, 500

        return photo.json(), 201

    def delete(self, name):
        photo = PhotoModel.find_by_name(name)
        if photo:
            photo.delete_from_db()
            return {'message': 'Photo deleted.'}
        return {'message': 'Photo not found.'}, 404

    def put(self, name):
        data = Photo.parser.parse_args()

        photo = PhotoModel.find_by_name(name)

        if photo:
            photo.url = data['url']
        else:
            photo = PhotoModel(name, **data)

        photo.save_to_db()

        return photo.json()


class PhotoList(Resource):
    def get(self):
        return {'photos': list(map(lambda x: x.json(), PhotoModel.query.all()))}