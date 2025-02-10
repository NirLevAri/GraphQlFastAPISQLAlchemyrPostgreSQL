from sqlalchemy.orm import Session
from app.modules.issue.models import Issue
from app.modules.issue.schemas import IssueCreate, IssueUpdate

class IssueService:
    def __init__(self, db: Session):
        self.db = db

    def create_issue(self, issue_data: IssueCreate) -> Issue:
        db_issue = Issue(
            title=issue_data.title,
            description=issue_data.description
        )
        self.db.add(db_issue)
        self.db.commit()
        self.db.refresh(db_issue)
        return db_issue

    def get_issues(self) -> list[Issue]:
        return self.db.query(Issue).all()

    def get_issue(self, issue_id: int) -> Issue | None:
        return self.db.query(Issue).filter(Issue.id == issue_id).first()

    def update_issue(self, issue_id: int, issue_data: IssueUpdate) -> Issue | None:
        issue = self.db.query(Issue).filter(Issue.id == issue_id).first()
        if not issue:
            return None
        if issue_data.title is not None:
            issue.title = issue_data.title
        if issue_data.description is not None:
            issue.description = issue_data.description
        self.db.commit()
        self.db.refresh(issue)
        return issue

    def delete_issue(self, issue_id: int) -> bool:
        issue = self.db.query(Issue).filter(Issue.id == issue_id).first()
        if not issue:
            return False
        self.db.delete(issue)
        self.db.commit()
        return True
