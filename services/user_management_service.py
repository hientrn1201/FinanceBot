import datetime
from database.services.user_service import UserService


class UserManagementService():
    def __init__(self, session):
        self.session = session
        self.init_service()

    def init_service(self):
        self.user_service = UserService(self.session)

    def create_user(self, id, user_name):
        user = self.user_service.create(
            id=id,
            user_name=user_name,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        return user

    def get_user(self, **filter_info):
        user = self.user_service.find(**filter_info)[0]

        return user

    def get_user_by_id(self, id):
        user = self.user_service.find_by_id(id)

        return user
