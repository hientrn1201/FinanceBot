from database.models import Category
from database.services.base import BaseService
from sqlalchemy.orm import Session


class CategoryService(BaseService):
    def __init__(self, session: Session) -> None:
        self.session = session
        self.model = Category
