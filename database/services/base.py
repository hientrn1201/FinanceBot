from sqlalchemy.orm import Session
from sqlalchemy.orm import load_only
from sqlalchemy import exc


class BaseService(object):
    session: Session = None
    model = None

    def find_by_id(self, model_id):
        query = self.session.query(self.model).filter(
            self.model.id == model_id
        )
        return query.first()

    def find(self, select_columns=None, **conditions):
        query = self.select_query(select_columns)

        for key, value in conditions.items():
            if isinstance(value, list):
                query = query.filter(getattr(self.model, key).in_(value))
                continue
            query = query.filter(getattr(self.model, key) == value)

        return query.all()

    def find_paging(
            self, limit=None, offset=None, select_columns=None, **conditions
    ):
        query = self.select_query(select_columns)
        for key, value in conditions.items():
            if isinstance(value, list):
                query = query.filter(getattr(self.model, key).in_(value))
                continue
            query = query.filter(getattr(self.model, key) == value)

        if limit is not None and offset is not None:
            return query.count(), query.limit(limit).offset(offset).all()
        else:
            records = query.all()
            return len(records), records

    def first(self, select_columns=None, **conditions):
        query = self.select_query(select_columns)
        for key, value in conditions.items():
            if isinstance(value, list):
                query = query.filter(getattr(self.model, key).in_(value))
                continue
            query = query.filter(getattr(self.model, key) == value)

        return query.first()

    def select_query(self, select_columns):
        sql_string = self.session.query(self.model)
        if select_columns is not None:
            sql_string = sql_string.options(load_only(*select_columns))
        return sql_string

    def create(self, mapping=None, model=None, **data):
        try:
            if model:
                obj = model()
            else:
                obj = self.model()

            for key in data:
                p = key
                if mapping and key in mapping:
                    p = mapping.get(key)

                if hasattr(obj, key):
                    setattr(obj, key, data[p])
            self.session.add(obj)
            self.session.commit()
            self.session.refresh(obj)
            return obj
        except exc.IntegrityError as e:
            raise e

    def update(self, obj, only=None, **data):
        if obj:
            for k in data:
                if hasattr(obj, k) and (only is None or k in only):
                    setattr(obj, k, data.get(k))
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, obj):
        try:
            self.session.delete(obj)
            self.session.commit()
            return True
        except exc.IntegrityError as e:
            raise e

    def delete_by_condition(self, **conditions):
        query = self.session.query(self.model)
        for key, value in conditions.items():
            if isinstance(value, list):
                query = query.filter(getattr(self.model, key).in_(value))
                continue
            query = query.filter(getattr(self.model, key) == value)
        try:
            query.delete()
            self.session.commit()
            return True
        except exc.IntegrityError as e:
            raise e
