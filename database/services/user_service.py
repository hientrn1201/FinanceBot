from models import User
from base import BaseService
from sqlalchemy.orm import Session


class UserService(BaseService):
    def __init__(self, session: Session) -> None:
        self.session = session
        self.model = User
