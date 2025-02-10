from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.db import Base
from app.modules.api_issue_association.models import api_issue_association

class API(Base):
    __tablename__ = "apis"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    # Many-to-many relationship with issues
    issues = relationship("Issue", secondary=api_issue_association, back_populates="apis", lazy="select")
