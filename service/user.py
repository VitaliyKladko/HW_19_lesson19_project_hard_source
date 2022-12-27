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

    def get_get_by_email(self, email):
        """
        Метод сервиса обращается к DAO, передает туда email и DAO отдает объект user
        """
        return self.dao.get_user_by_email(email)

    def create_user(self, data: dict):
        # перезаписываем password в dict и добавлем сущность в БД с помощью UserDAO
        data['password'] = self.get_hash(data.get('password'))
        return self.dao.create(data)

    def delete(self, uid):
        return self.dao.delete(uid)

    def update(self, data_json: dict):
        user_to_update = self.get_one_user(data_json['id'])

        if data_json.get('name') is not None:
            user_to_update.name = data_json.get('name')

        if data_json.get('surname') is not None:
            user_to_update.surname = data_json.get('surname')

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

    def auth_user(self, email, password):
        user_by_email = self.get_get_by_email(email)

        if user_by_email is None:
            return None

        password_hash = self.get_hash(password)

        if password_hash != user_by_email.password:
            return None

        user_data = {
            'email': user_by_email.email
        }
        tokens = self.get_tokens(user_data)
        return tokens

    def refresh_update_tokens(self, refresh_token: str):
        """
        Метод декодирует refresh_token, создает новую пару токенов и отдает их
        """
        try:
            user_data = jwt.decode(jwt=refresh_token, key=Config.SECRET_HERE, algorithms=[Config.ALGO])
        except Exception as e:
            return None

        return self.get_tokens(user_data)

    def get_user_email_from_token(self, header):
        token = header.split('Bearer ')[-1]
        user_data = jwt.decode(token, Config.SECRET_HERE, algorithms=[Config.ALGO])

        user_email = user_data.get('email')

        return user_email

    def change_password(self, req_json):
        """
        Производит замену password если были переданы password_1 и password_2 и password_1 совпадает с password в БД
        """
        old_password_hash = self.get_hash(req_json.get('password_1'))
        user = self.get_one_user(req_json.get('id'))

        if user.password == old_password_hash:
            req_json['password_2'] = self.get_hash(req_json['password_2'])
            self.dao.change_password(req_json, user)
