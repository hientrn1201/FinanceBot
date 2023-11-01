from database.services.categories import CategoryService


class CategoryManagementService():
    def __init__(self, session, user_management_service) -> None:
        self.session = session
        self.user_management_service = user_management_service
        self.init_service()

    def init_service(self):
        self.category_service = CategoryService(self.session)

    def create_category(self, user_id, description):
        user = self.user_management_service.get_user_by_id(user_id)

        if not user:
            raise Exception("User not found")

        category = self.category_service.create(
            user_id=user.id,
            description=description,
        )

        return category

    def get_categories(self, **filter_info):
        if filter_info['user_id']:
            user = self.user_management_service.get_user_by_id(
                filter_info['user_id'])

            if not user:
                raise Exception("User not found")

        categories = self.category_service.find(**filter_info)

        return categories

    def get_category_by_id(self, category_id):
        category = self.category_service.find_by_id(category_id)

        if not category:
            return None

        return category

    def update_category(self, category_id, **data):
        category = self.category_service.find_by_id(category_id)

        if not category:
            raise Exception("Category not found")

        category = self.category_service.update(
            category,
            **data,
        )

        return category

    def delete_category(self, category_id):
        category = self.category_service.find_by_id(category_id)

        if not category:
            raise Exception("Category not found")

        self.category_service.delete(category)

        return True
