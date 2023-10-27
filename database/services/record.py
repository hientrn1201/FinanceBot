from database.models import Record
from database.services.base import BaseService
from sqlalchemy.orm import Session


class RecordService(BaseService):
    def __init__(self, session: Session) -> None:
        self.session = session
        self.model = Record
