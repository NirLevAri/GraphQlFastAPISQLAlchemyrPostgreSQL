from sqlalchemy.orm import Session
from app.modules.api.models import API
from app.modules.issue.models import Issue

class AssociationService:
    def __init__(self, db: Session):
        self.db = db

    def add_issue_to_api(self, api_id: int, issue_id: int) -> dict:
        api = self.db.query(API).filter(API.id == api_id).first()
        if not api:
            raise Exception("API not found")
        issue = self.db.query(Issue).filter(Issue.id == issue_id).first()
        if not issue:
            raise Exception("Issue not found")
        if issue in api.issues:
            return {"detail": "Issue already associated with API"}
        api.issues.append(issue)
        self.db.commit()
        self.db.refresh(api)
        return {"detail": "Issue added to API", "api_id": api_id, "issue_id": issue_id}

    def remove_issue_from_api(self, api_id: int, issue_id: int) -> dict:
        api = self.db.query(API).filter(API.id == api_id).first()
        if not api:
            raise Exception("API not found")
        issue = self.db.query(Issue).filter(Issue.id == issue_id).first()
        if not issue:
            raise Exception("Issue not found")
        if issue not in api.issues:
            return {"detail": "Issue is not associated with API"}
        api.issues.remove(issue)
        self.db.commit()
        self.db.refresh(api)
        return {"detail": "Issue removed from API", "api_id": api_id, "issue_id": issue_id}
