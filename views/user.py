from flask_restx import Resource, Namespace
from flask import request

from dao.model.user import UserSchema
from implemented import user_service


user_ns = Namespace('users')
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        all_users = user_service.get_all_users()
        return users_schema.dump(all_users), 200

    def post(self):
        req_json = request.json
        try:
            user = user_service.create_user(req_json)
            return '', 201, {"location": f"/users/{user.id}"}
        except Exception as e:
            return {"error": f"{e}"}, 400


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        user_by_id = user_service.get_one_user(uid)

        if user_by_id is None:
            return {"error": "User not found"}, 404

        return user_schema.dump(user_by_id), 200

    def put(self, uid):
        req_json = request.json
        req_json['id'] = uid

        fields = ['username', 'password', 'role']

        for field in fields:
            if field not in req_json:
                return {"error": f"Поле {field} обязательно"}, 400

        user_service.update(req_json)
        return '', 204

    def delete(self, uid):
        user_to_delete = user_service.get_one_user(uid)

        if user_to_delete is None:
            return {"error": "User not found"}, 404

        user_service.delete(uid)
        return '', 204
