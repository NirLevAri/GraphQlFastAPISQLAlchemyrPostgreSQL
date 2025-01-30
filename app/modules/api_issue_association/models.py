from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.db import Base

class API_Issue_Association(Base):
    __tablename__ = "api_issue_association"

    api_id = Column(Integer, ForeignKey("apis.id"), primary_key=True)
    issue_id = Column(Integer, ForeignKey("issues.id"), primary_key=True)

    api = relationship("API", back_populates="issues")
    issue = relationship("Issue", back_populates="apis")
