from database.services.user import UserService


class UserManagementService():
    def __init__(self, session):
        self.session = session
        self.init_service()

    def init_service(self):
        self.user_service = UserService(self.session)

    def create_user(self, id, last_name, first_name):
        user = self.user_service.create(
            id=id,
            last_name=last_name,
            first_name=first_name,
        )

        return user

    def get_user(self, **filter_info):
        user = self.user_service.find(**filter_info)[0]

        return user

    def get_user_by_id(self, id):
        user = self.user_service.find_by_id(id)

        return user
