from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.modules.issue.schemas import IssueCreate, IssueUpdate, IssueOut
from app.modules.issue.services import issue_service

router = APIRouter(prefix="/issues", tags=["Issues"])

@router.post("/", response_model=IssueOut)
def create_issue(issue: IssueCreate, db: Session = Depends(get_db)):
    return issue_service.create_issue(db, issue)

@router.get("/", response_model=list[IssueOut])
def read_issues(db: Session = Depends(get_db)):
    return issue_service.get_issues(db)

@router.get("/{issue_id}", response_model=IssueOut)
def read_issue(issue_id: int, db: Session = Depends(get_db)):
    issue = issue_service.get_issue(db, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue

@router.put("/{issue_id}", response_model=IssueOut)
def update_issue(issue_id: int, issue_update: IssueUpdate, db: Session = Depends(get_db)):
    issue = issue_service.update_issue(db, issue_id, issue_update)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue

@router.delete("/{issue_id}")
def delete_issue(issue_id: int, db: Session = Depends(get_db)):
    if not issue_service.delete_issue(db, issue_id):
        raise HTTPException(status_code=404, detail="Issue not found")
    return {"detail": "Issue deleted"}
