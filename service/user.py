import hashlib
import base64
import calendar
import datetime
import jwt


from dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from config import Config


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one_user(self, uid):
        return self.dao.get_one_user(uid)

    def get_all_users(self):
        return self.dao.get_all_users()

    def create_user(self, data: dict):
        # перезаписываем password в dict и добавлем сущность в БД с помощью UserDAO
        data['password'] = self.get_hash(data.get('password'))
        return self.dao.create(data)

    def delete(self, uid):
        return self.dao.delete(uid)

    def update(self, data_json: dict):
        user_to_update = self.get_one_user(data_json['id'])

        user_to_update.username = data_json['username']
        user_to_update.password = data_json['password']
        user_to_update.role = data_json['role']

        self.dao.update(user_to_update)

    def get_hash(self, password: str):
        """
        Метод создает хеш пароля и он исп. при добавлении в БД уже хешированного пароля при создании пользователя
        """
        password_blob = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return base64.b64encode(password_blob)

    def get_tokens(self, user_obj: dict):
        """
        Метод получает payload сущности user типа:  {"username": user.username, "role": user.role} и генерит пару access
        и refresh токен и отдает их в dict.
        """
        # создаем access_token
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        user_obj["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(user_obj, Config.SECRET_HERE, algorithm=Config.ALGO)

        # создаем refresh_token
        day30 = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        user_obj["exp"] = calendar.timegm(day30.timetuple())
        refresh_token = jwt.encode(user_obj, Config.SECRET_HERE, algorithm=Config.ALGO)

        return {"access_token": access_token, "refresh_token": refresh_token}

    def auth_user(self, username, password):
        """
        Проверяет соотвествие с данными в БД (есть ли такой пользователь, такой ли у него пароль) и если всё оk —
        генерит пару access_token и refresh_token и отдает из в AuthView.
        """
        # получаем пользователя с помощью DAO по имени пользователя
        user_auth = self.dao.get_by_username(username)

        # если пользователь не найден, отдаем None
        if user_auth is None:
            return None

        # сравниваем пароль в БД с паролем при авторизации
        password_hash = self.get_hash(password)
        if password_hash != user_auth.password:
            return None

        user_obj = {
            'username': user_auth.username,
            'role': user_auth.role
        }

        return self.get_tokens(user_obj)

    def refresh_update_tokens(self, refresh_token: str):
        """
        Метод декодирует refresh_token, получает данные из БД по имени пользователя, создает новую пару токенов и отдает
        их
        """
        try:
            user_data = jwt.decode(jwt=refresh_token, key=Config.SECRET_HERE, algorithms=[Config.ALGO])
        except Exception as e:
            return None

        user = self.dao.get_by_username(user_data.get('username'))

        user_obj = {
            'username': user.username,
            'role': user.role
        }

        return self.get_tokens(user_obj)
