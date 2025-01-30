# app/contexts/api/repositories.py
from sqlalchemy.orm import Session
from .models import API

class APIRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_api(self, path: str, host: str, method: str) -> API:
        new_api = API(path=path, host=host, method=method)
        self.db.add(new_api)
        self.db.commit()
        self.db.refresh(new_api)
        return new_api

    def get_api(self, api_id: int) -> API | None:
        return self.db.query(API).filter(API.id == api_id).first()

    def list_apis(self) -> list[API]:
        return self.db.query(API).all()

    def update_api(self, api_id: int, **fields) -> API | None:
        api_obj = self.get_api(api_id)
        if not api_obj:
            return None
        for field, value in fields.items():
            if value is not None:
                setattr(api_obj, field, value)
        self.db.commit()
        self.db.refresh(api_obj)
        return api_obj

    def delete_api(self, api_id: int) -> bool:
        api_obj = self.get_api(api_id)
        if api_obj:
            self.db.delete(api_obj)
            self.db.commit()
            return True
        return False
