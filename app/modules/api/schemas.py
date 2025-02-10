from pydantic import BaseModel
from typing import List, Optional

class APIBase(BaseModel):
    name: str
    description: Optional[str] = None

class APICreate(APIBase):
    pass

class APIUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class APIOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    issues: Optional[List["IssueOut"]] = None

    class Config:
        orm_mode = True

from app.modules.issue.schemas import IssueOut
APIOut.update_forward_refs()
