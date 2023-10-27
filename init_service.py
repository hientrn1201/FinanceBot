from services.process_chat_service import ProcessChatService
from services.user_management_service import UserManagementService
from services.record_service import RecordManagementService
from services.category_service import CategoryManagementService


def init_services(session):
    user_management_service = UserManagementService(session)
    category_management_service = CategoryManagementService(
        session, user_management_service)
    record_management_service = RecordManagementService(
        session, user_management_service, category_management_service)
    process_chat_service = ProcessChatService(
        session, user_management_service, record_management_service, category_management_service)

    return process_chat_service
