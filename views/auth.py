from flask_restx import Resource, Namespace
from flask import request, abort

from implemented import user_service


auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        """
        Получает логин и пароль из Body запроса в виде JSON, c помощью user сервиса делает проверку о наличии такого
        пользовател в БД, сверяет его пароль и отдает access и refresh токены
        """
        req_json = request.json
        login = req_json.get('username')
        password = req_json.get('password')

        # Ошибка 400 bad request говорит о том, что сервер сайта не понял запрос, который отправил пользователь
        # по дефолту метод get у dict отдает None, если ключ не найден в dict
        if None in [login, password]:
            abort(400)

        tokens = user_service.auth_user(username=login, password=password)

        # 401 Unauthorized Error («отказ в доступе») при открытии страницы сайта означает неверную авторизацию или
        # аутентификацию пользователя
        if tokens is None:
            abort(401)

        return tokens, 201

    def put(self):
        req_json = request.json
        refresh_token = req_json.get('refresh_token')

        # Ошибка 400 bad request
        if refresh_token is None:
            abort(400)

        tokens = user_service.refresh_update_tokens(refresh_token)

        # 401 Unauthorized Error
        if tokens is None:
            return {"error": "Неверные учётные данные"}, 401

        return tokens, 201
