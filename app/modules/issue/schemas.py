from pydantic import BaseModel
from typing import List, Optional

class IssueBase(BaseModel):
    title: str
    description: Optional[str] = None

class IssueCreate(IssueBase):
    pass

class IssueUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class IssueOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    apis: Optional[List["APIOut"]] = None

    class Config:
       from_attributes = True

from app.modules.api.schemas import APIOut
IssueOut.update_forward_refs()
