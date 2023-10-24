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

    def create(self, flush=True, mapping=None, model=None, **data):
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
            if 'id' not in data:
                obj.id = str(uuid.uuid4())
            self.session.add(obj)
            if flush:
                self.session.flush()
            return obj
        except exc.IntegrityError as e:
            raise e

    def bulk_create(self, object_infos, model=None):
        if not model:
            model = self.model
        for i in range(len(object_infos)):
            if 'id' not in object_infos[i]:
                object_infos[i]['id'] = str(uuid.uuid4())
        return self.session.bulk_insert_mappings(
            model,
            object_infos,
            return_defaults=True
        )

    def update(self, obj, flush=True, only=None, **data):
        if obj:
            for k in data:
                if hasattr(obj, k) and (only is None or k in only):
                    setattr(obj, k, data.get(k))
        if flush:
            self.session.flush()
        return obj

    def bulk_update(self, records, model=None):
        if not model:
            model = self.model
        return self.session.bulk_update_mappings(model, records)

    def upsert(self, filter_info, new_info):
        new_objects = self.find(
            **filter_info
        )
        if not new_objects:
            new_objects = [self.create(**new_info)]
            return new_objects
        for new_object in new_objects:
            self.update(
                new_object,
                **new_info
            )
        return new_objects

    def delete(self, obj, flush=True):
        try:
            self.session.delete(obj)
            if flush:
                self.session.flush()
            return True
        except exc.IntegrityError as e:
            raise e

    def delete_by_condition(self, flush=True, **conditions):
        query = self.session.query(self.model)
        for key, value in conditions.items():
            if isinstance(value, list):
                query = query.filter(getattr(self.model, key).in_(value))
                continue
            query = query.filter(getattr(self.model, key) == value)
        try:
            query.delete()
            if flush:
                self.session.flush()
            return True
        except exc.IntegrityError as e:
            raise e
