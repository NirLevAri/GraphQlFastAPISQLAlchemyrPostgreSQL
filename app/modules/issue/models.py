from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from app.core.db import Base

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)

    apis = relationship("API_Issue_Association", back_populates="issue")
