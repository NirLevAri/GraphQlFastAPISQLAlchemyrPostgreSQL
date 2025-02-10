from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.modules.api.schemas import APICreate, APIUpdate, APIOut
from app.modules.api.services import APIService

router = APIRouter(prefix="/apis", tags=["APIs"])

@router.post("/", response_model=APIOut)
def create_api(api_data: APICreate, db: Session = Depends(get_db)):
    service = APIService(db)
    return service.create_api(api_data)

@router.get("/", response_model=List[APIOut])
def read_apis(include_issues: bool = False, db: Session = Depends(get_db)):
    service = APIService(db)
    return service.get_apis(include_issues=include_issues)

@router.get("/{api_id}", response_model=APIOut)
def read_api(api_id: int, db: Session = Depends(get_db)):
    service = APIService(db)
    api = service.get_api(api_id)
    if not api:
        raise HTTPException(status_code=404, detail="API not found")
    return api

@router.put("/{api_id}", response_model=APIOut)
def update_api(api_id: int, api_data: APIUpdate, db: Session = Depends(get_db)):
    service = APIService(db)
    api = service.update_api(api_id, api_data)
    if not api:
        raise HTTPException(status_code=404, detail="API not found")
    return api

@router.delete("/{api_id}")
def delete_api(api_id: int, db: Session = Depends(get_db)):
    service = APIService(db)
    if not service.delete_api(api_id):
        raise HTTPException(status_code=404, detail="API not found")
    return {"detail": "API deleted"}
