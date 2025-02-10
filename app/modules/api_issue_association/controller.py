from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.modules.api_issue_association.services import AssociationService

router = APIRouter(prefix="/associations", tags=["Associations"])

@router.post("/add_issue")
def add_issue_to_api(api_id: int, issue_id: int, db: Session = Depends(get_db)):
    service = AssociationService(db)
    try:
        result = service.add_issue_to_api(api_id, issue_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return result

@router.post("/remove_issue")
def remove_issue_from_api(api_id: int, issue_id: int, db: Session = Depends(get_db)):
    service = AssociationService(db)
    try:
        result = service.remove_issue_from_api(api_id, issue_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return result
