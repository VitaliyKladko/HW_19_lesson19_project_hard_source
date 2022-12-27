from flask_restx import Resource, Namespace
from flask import request, abort

from implemented import user_service


auth_ns = Namespace('auth')


@auth_ns.route('/register')
class AuthView(Resource):
    """
    Передавая  email и пароль, создаем пользователя в системе, хешируя password в БД
    """
    def post(self):
        req_json = request.json
        try:
            user = user_service.create_user(req_json)
            return "", 201, {"location": f"/users/{user.id}"}
        except Exception as e:
            return {"error": f"{e}"}, 400


@auth_ns.route('/login')
class AuthView(Resource):
    def post(self):
        """
        Проверка email и password в БД, отдает пару access_token, refresh_token
        """
        req_json = request.json
        email = req_json.get('email')
        password = req_json.get('password')

        if None in [email, password]:
            abort(400)

        tokens = user_service.auth_user(email, password)

        if tokens is None:
            return {"error": "Неверные учётные данные"}, 401

        return tokens, 201

    def put(self):
        """
        Отдает пару токенов после проверки валидности refresh_token. Если токен помер, то отдает код 401
        """
        req_json = request.json
        refresh_token = req_json.get('refresh_token')

        if refresh_token is None:
            abort(400)

        tokens = user_service.refresh_update_tokens(refresh_token)

        if tokens is None:
            return {"error": "Неверные учётные данные"}, 401

        return tokens, 201
