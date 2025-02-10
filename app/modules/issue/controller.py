from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.modules.issue.schemas import IssueCreate, IssueUpdate, IssueOut
from app.modules.issue.services import IssueService

router = APIRouter(prefix="/issues", tags=["Issues"])

@router.post("/", response_model=IssueOut)
def create_issue_endpoint(issue: IssueCreate, db: Session = Depends(get_db)):
    service = IssueService(db)
    return service.create_issue(issue)

@router.get("/", response_model=List[IssueOut])
def read_issues_endpoint(db: Session = Depends(get_db)):
    service = IssueService(db)
    return service.get_issues()

@router.get("/{issue_id}", response_model=IssueOut)
def read_issue_endpoint(issue_id: int, db: Session = Depends(get_db)):
    service = IssueService(db)
    issue = service.get_issue(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue

@router.put("/{issue_id}", response_model=IssueOut)
def update_issue_endpoint(issue_id: int, issue_update: IssueUpdate, db: Session = Depends(get_db)):
    service = IssueService(db)
    issue = service.update_issue(issue_id, issue_update)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue

@router.delete("/{issue_id}")
def delete_issue_endpoint(issue_id: int, db: Session = Depends(get_db)):
    service = IssueService(db)
    if not service.delete_issue(issue_id):
        raise HTTPException(status_code=404, detail="Issue not found")
    return {"detail": "Issue deleted"}
