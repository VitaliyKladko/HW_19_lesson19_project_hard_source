from flask_restx import Resource, Namespace
from flask import request

from dao.model.director import DirectorSchema
from implemented import director_service
from decorators import auth_required, admin_required

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.json
        try:
            director = director_service.create(req_json)
            return '', 201, {"location": f"/directors/{director.id}"}
        except Exception as e:
            return {"error": f"{e}"}, 400

@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    @auth_required
    def get(self, rid):
        r = director_service.get_one(rid)

        if r is None:
            return {"error": "Director not found"}, 404

        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, rid):
        req_json = request.json
        req_json['id'] = rid

        fields = ['name']

        for field in fields:
            if field not in req_json:
                return {"error": f"Поле {field} обязательно"}, 400

        director_service.update(req_json)
        return '', 204

    @admin_required
    def delete(self, rid):
        director_to_delete = director_service.get_one(rid)

        if director_to_delete is None:
            return {"error": "Director not found"}, 404

        director_service.delete(rid)
        return '', 204
