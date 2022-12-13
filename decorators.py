import jwt
from flask import abort, request
from config import Config


def auth_required(func):
    """
    Декоратор запрашивает авторизацию по access_token (Authorized Required)
    """
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, Config.SECRET_HERE, algorithms=Config.ALGO)
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):

        # 401 Unauthorized («не авторизован (не представился))
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        role = None
        try:
            data = jwt.decode(token, Config.SECRET_HERE, algorithms=Config.ALGO)
            role = data['role']
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)

        # 403 Forbidden («запрещено (не уполномочен))»
        if role != 'admin':
            abort(403)

        return func(*args, **kwargs)

    return wrapper

