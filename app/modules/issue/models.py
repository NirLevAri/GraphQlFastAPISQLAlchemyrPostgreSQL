from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.db import Base
from app.modules.api_issue_association import api_issue_association

class Issue(Base):
    __tablename__ = "issues"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    apis = relationship("API", secondary=api_issue_association, back_populates="issues", lazy="select")
