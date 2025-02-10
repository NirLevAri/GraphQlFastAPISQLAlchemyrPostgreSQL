from sqlalchemy.orm import Session, joinedload
from app.modules.api.models import API
from app.modules.api.schemas import APICreate, APIUpdate

class APIService:
    def __init__(self, db: Session):
        self.db = db

    def create_api(self, api_data: APICreate) -> API:
        db_api = API(name=api_data.name, description=api_data.description)
        self.db.add(db_api)
        self.db.commit()
        self.db.refresh(db_api)
        return db_api

    def get_apis(self, include_issues: bool = False) -> list[API]:
        query = self.db.query(API)
        if include_issues:
            query = query.options(joinedload(API.issues))
        return query.all()

    def get_api(self, api_id: int) -> API | None:
        return self.db.query(API).filter(API.id == api_id).first()

    def update_api(self, api_id: int, api_data: APIUpdate) -> API | None:
        api = self.db.query(API).filter(API.id == api_id).first()
        if not api:
            return None
        if api_data.name is not None:
            api.name = api_data.name
        if api_data.description is not None:
            api.description = api_data.description
        self.db.commit()
        self.db.refresh(api)
        return api

    def delete_api(self, api_id: int) -> bool:
        api = self.db.query(API).filter(API.id == api_id).first()
        if not api:
            return False
        self.db.delete(api)
        self.db.commit()
        return True
