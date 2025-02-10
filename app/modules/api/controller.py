from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.modules.api.schemas import APICreate, APIUpdate, APIOut
from app.modules.api.services import api_service

router = APIRouter(prefix="/apis", tags=["APIs"])

@router.post("/", response_model=APIOut)
def create_api(api: APICreate, db: Session = Depends(get_db)):
    return api_service.create_api(db, api)

@router.get("/", response_model=list[APIOut])
def read_apis(include_issues: bool = Query(False, description="Include associated issues"),
              db: Session = Depends(get_db)):
    return api_service.get_apis(db, include_issues)

@router.get("/{api_id}", response_model=APIOut)
def read_api(api_id: int, db: Session = Depends(get_db)):
    api = api_service.get_api(db, api_id)
    if not api:
        raise HTTPException(status_code=404, detail="API not found")
    return api

@router.put("/{api_id}", response_model=APIOut)
def update_api(api_id: int, api_update: APIUpdate, db: Session = Depends(get_db)):
    api = api_service.update_api(db, api_id, api_update)
    if not api:
        raise HTTPException(status_code=404, detail="API not found")
    return api

@router.delete("/{api_id}")
def delete_api(api_id: int, db: Session = Depends(get_db)):
    if not api_service.delete_api(db, api_id):
        raise HTTPException(status_code=404, detail="API not found")
    return {"detail": "API deleted"}
