from flask_restx import Resource, Namespace
from flask import request

from dao.model.genre import GenreSchema
from implemented import genre_service
from decorators import auth_required, admin_required

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.json
        try:
            new_genre = genre_service.create(req_json)
            return '', 201, {"location": f"/genres/{new_genre.id}"}
        except Exception as e:
            return {"error": f"{e}"}, 400


@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    @auth_required
    def get(self, rid):
        r = genre_service.get_one(rid)

        if r is None:
            return {"error": "Genre not found"}, 404

        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, rid):
        req_json = request.json
        req_json['id'] = rid

        fields = ['name']

        for field in fields:
            if field not in req_json:
                return {"error": f"Поле {field} обязательно"}, 400

        genre_service.update(req_json)
        return '', 204

    @admin_required
    def delete(self, rid):
        genre_to_delete = genre_service.get_one(rid)

        if genre_to_delete is None:
            return {"error": "Genre not found"}, 404

        genre_service.delete(rid)
        return '', 204
