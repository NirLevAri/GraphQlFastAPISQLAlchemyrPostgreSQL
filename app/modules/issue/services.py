from sqlalchemy.orm import Session
from app.modules.issue.models import Issue
from app.modules.issue.schemas import IssueCreate, IssueUpdate

def create_issue(db: Session, issue_data: IssueCreate):
    db_issue = Issue(title=issue_data.title, description=issue_data.description)
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue

def get_issues(db: Session):
    return db.query(Issue).all()

def get_issue(db: Session, issue_id: int):
    return db.query(Issue).filter(Issue.id == issue_id).first()

def update_issue(db: Session, issue_id: int, issue_data: IssueUpdate):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        return None
    if issue_data.title is not None:
        issue.title = issue_data.title
    if issue_data.description is not None:
        issue.description = issue_data.description
    db.commit()
    db.refresh(issue)
    return issue

def delete_issue(db: Session, issue_id: int):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        return False
    db.delete(issue)
    db.commit()
    return True
