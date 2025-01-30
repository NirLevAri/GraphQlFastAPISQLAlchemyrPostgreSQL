from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import Base

class API(Base):
    __tablename__ = "apis"

    id = Column(Integer, primary_key=True, index=True)
    host = Column(String, nullable=False)
    path = Column(String, nullable=False)
    method = Column(String, nullable=False)

    issues = relationship("API_Issue_Association", back_populates="api")
