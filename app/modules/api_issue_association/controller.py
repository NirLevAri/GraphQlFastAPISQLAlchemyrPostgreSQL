from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.modules.api.models import API
from app.modules.issue.models import Issue

router = APIRouter(prefix="/associations", tags=["Associations"])

@router.post("/add_issue")
def add_issue_to_api(api_id: int, issue_id: int, db: Session = Depends(get_db)):
    api = db.query(API).filter(API.id == api_id).first()
    if not api:
        raise HTTPException(status_code=404, detail="API not found")
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    if issue in api.issues:
        return {"detail": "Issue already associated with API"}
    api.issues.append(issue)
    db.commit()
    db.refresh(api)
    return {"detail": "Issue added to API", "api_id": api_id, "issue_id": issue_id}

@router.post("/remove_issue")
def remove_issue_from_api(api_id: int, issue_id: int, db: Session = Depends(get_db)):
    api = db.query(API).filter(API.id == api_id).first()
    if not api:
        raise HTTPException(status_code=404, detail="API not found")
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    if issue not in api.issues:
        return {"detail": "Issue is not associated with API"}
    api.issues.remove(issue)
    db.commit()
    db.refresh(api)
    return {"detail": "Issue removed from API", "api_id": api_id, "issue_id": issue_id}
