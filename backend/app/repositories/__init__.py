from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

class BaseRepo:
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model
    def get(self, id: UUID):
        pk = list(self.model.__table__.primary_key.columns)[0].name
        return self.db.query(self.model).filter(getattr(self.model, pk) == id).first()
    def list(self, skip=0, limit=20):
        q = self.db.query(self.model)
        total = q.count()
        items = q.offset(skip).limit(limit).all()
        return items, total
    def create(self, obj):
        self.db.add(obj); self.db.commit(); self.db.refresh(obj); return obj
    def update(self, obj, data: dict):
        for k,v in data.items():
            if v is not None: setattr(obj, k, v)
        self.db.commit(); self.db.refresh(obj); return obj
