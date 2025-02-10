from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.db import Base

api_issue_association = Table(
    "api_issue_association",
    Base.metadata,
    Column("api_id", Integer, ForeignKey("apis.id"), primary_key=True),
    Column("issue_id", Integer, ForeignKey("issues.id"), primary_key=True)
)
