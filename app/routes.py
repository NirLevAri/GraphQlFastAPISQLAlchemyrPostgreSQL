from fastapi import APIRouter
from app.modules.api.controller import router as api_controller
from app.modules.issue.controller import router as issue_controller
from app.modules.api_issue_association.controller import router as association_controller

router = APIRouter()
router.include_router(api_controller)
router.include_router(issue_controller)
router.include_router(association_controller)
