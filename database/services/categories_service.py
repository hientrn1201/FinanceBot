import datetime
from sqlalchemy.orm import Session
from models import Category
import schemas


def create_category(db: Session, category: schemas.CategoryRequest):
    db_category = Category(
        user_id=category.user_id,
        description=category.description,
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def update_category(db: Session, category_id: int, **data):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        return None
    for key, value in data.items():
        setattr(db_category, key, value)

    db_category.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        return None
    db.delete(db_category)
    db.commit()
    return db_category
