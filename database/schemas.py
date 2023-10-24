from pydantic import BaseModel


class UserRequest(BaseModel):
    platform: str
    platform_id: str
    name: str


class CategoryRequest(BaseModel):
    user_id: int
    description: str


class RecordRequest(BaseModel):
    user_id: int
    category_id: int
    note: str
    amount: int
