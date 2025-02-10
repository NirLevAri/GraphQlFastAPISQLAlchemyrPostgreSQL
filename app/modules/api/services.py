from sqlalchemy.orm import Session
from app.modules.api.models import API
from app.modules.api.schemas import APICreate, APIUpdate
from sqlalchemy.orm import joinedload

def create_api(db: Session, api_data: APICreate):
    db_api = API(name=api_data.name, description=api_data.description)
    db.add(db_api)
    db.commit()
    db.refresh(db_api)
    return db_api

def get_apis(db: Session, include_issues: bool = False):
    query = db.query(API)
    if include_issues:
        query = query.options(joinedload(API.issues))
    return query.all()

def get_api(db: Session, api_id: int):
    return db.query(API).filter(API.id == api_id).first()

def update_api(db: Session, api_id: int, api_data: APIUpdate):
    api = db.query(API).filter(API.id == api_id).first()
    if not api:
        return None
    if api_data.name is not None:
        api.name = api_data.name
    if api_data.description is not None:
        api.description = api_data.description
    db.commit()
    db.refresh(api)
    return api

def delete_api(db: Session, api_id: int):
    api = db.query(API).filter(API.id == api_id).first()
    if not api:
        return False
    db.delete(api)
    db.commit()
    return True
