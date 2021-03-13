from flask_login import UserMixin
from.firestore_service import get_user

class UserData:
    def __init__(self, username, password, is_admin):
        self.username = username
        self.password = password
        self.is_admin = is_admin

class UserModel(UserMixin):
    def __init__(self, user_data):
        """
        ;param user_data: UserData
        """
        self.id = user_data.username
        self.password = user_data.password
        self.is_admin = user_data.is_admin

    @staticmethod
    def query(user_id):
        user_document = get_user(user_id)
        user_data = UserData(
            username=user_document.id,
            password=user_document.to_dict()['password'],
            is_admin=user_document.to_dict()['admin']
        )
        return UserModel(user_data)