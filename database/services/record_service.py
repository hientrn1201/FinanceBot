import datetime
from sqlalchemy.orm import Session
from models import Record
import schemas


def create_record(db: Session, record: schemas.RecordRequest):
    db_record = Record(
        user_id=record.user_id,
        category_id=record.category_id,
        description=record.description,
        amount=record.amount,
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def get_record(db: Session, record_id: int):
    return db.query(Record).filter(Record.id == record_id).first()


def update_record(db: Session, record_id: int, **data):
    db_record = db.query(Record).filter(Record.id == record_id).first()

    if not db_record:
        return None

    for key, value in data.items():
        setattr(db_record, key, value)

    db_record.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_record)
    return db_record
