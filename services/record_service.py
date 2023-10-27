from database.services.record import RecordService


class RecordManagementService():
    def __init__(self, session, user_management_service, category_management_service) -> None:
        self.session = session
        self.user_management_service = user_management_service
        self.category_management_service = category_management_service

        self.init_service()

    def init_service(self):
        self.record_service = RecordService(self.session)

    def create_record(self, user_id, category_id, amount, note):
        user = self.user_management_service.get_user_by_id(user_id)

        if not user:
            raise Exception("User not found")

        category = self.category_management_service.get_category_by_id(
            category_id)

        if not category:
            raise Exception("Category not found")

        record = self.record_service.create(
            user_id=user.id,
            category_id=category.id,
            amount=amount,
            note=note,
        )

        return record

    def get_record(self, **filter_info):
        if filter_info['user_id']:
            user = self.user_management_service.get_user_by_id(
                filter_info['user_id'])

            if not user:
                raise Exception("User not found")

        if filter_info['category_id']:
            category = self.category_management_service.get_category_by_id(
                filter_info['category_id'])

            if not category:
                raise Exception("Category not found")

        records = self.record_service.find(**filter_info)

        return records

    def update_record(self, record_id, **data):
        record = self.record_service.find_by_id(record_id)

        if not record:
            raise Exception("Record not found")

        record = self.record_service.update(
            record,
            **data,
        )

        return record

    def delete_record(self, record_id):
        record = self.record_service.find_by_id(record_id)

        if not record:
            raise Exception("Record not found")

        self.record_service.delete(record)
