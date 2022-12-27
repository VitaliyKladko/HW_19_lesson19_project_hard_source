from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one_user(self, uid):
        return self.session.query(User).get(uid)

    def get_all_users(self):
        return self.session.query(User).all()

    def get_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str):
        user = self.session.query(User).filter(User.email == email).first()
        return user

    def create(self, user_data: dict):
        new_user = User(**user_data)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def delete(self, uid):
        user_to_delete = self.get_one_user(uid)
        self.session.delete(user_to_delete)
        self.session.commit()

    def update(self, user: object):
        self.session.add(user)
        self.session.commit()

    def change_password(self, data, user):
        user.password = data.get('password_2')

        self.session.add(user)
        self.session.commit()
