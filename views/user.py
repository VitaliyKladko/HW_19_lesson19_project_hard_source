from flask_restx import Resource, Namespace
from flask import request, abort

from dao.model.user import UserSchema
from implemented import user_service
from decorators import auth_required


user_ns = Namespace('user')
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_ns.route('/')
class UserView(Resource):
    @auth_required
    def get(self):
        """
        Отдает информацию о пользователе (его профиль) в случае, если токен живой
        """
        req_header = request.headers['Authorization']

        user_email_from_token = user_service.get_user_email_from_token(req_header)

        if user_email_from_token is None:
            abort(401)

        user_profile_info = user_service.get_get_by_email(user_email_from_token)

        if user_profile_info is None:
            return {"error": "User not found"}, 404

        return user_schema.dump(user_profile_info), 200

    @auth_required
    def patch(self):
        """
        Делает частичное обновление данных user
        """
        req_json = request.json
        req_header = request.headers['Authorization']

        user_email = user_service.get_user_email_from_token(req_header)

        if user_email is None:
            abort(401)

        user = user_service.get_get_by_email(user_email)

        if "id" not in req_json:
            req_json['id'] = user.id

        user_service.update(req_json)

        return '', 204

@user_ns.route('/password')
class UserView(Resource):
    @auth_required
    def put(self):
        """
        Обновляет старый password_1 на password_2
        """
        req_json = request.json
        req_header = request.headers['Authorization']

        user_email = user_service.get_user_email_from_token(req_header)

        if user_email is None:
            abort(401)

        # объект user из БД по полученному email
        user_by = user_service.get_get_by_email(user_email)

        if "id" not in req_json:
            req_json['id'] = user_by.id

        if "password_1" not in req_json or "password_2" not in req_json:
            return {"error": "Поля password_1 и password_2 обязательны"}, 400

        user_service.change_password(req_json)

        return '', 204
