from fastapi import APIRouter

from api.v1.prompts import router as prompts_router

router = APIRouter(prefix="/api/v1")
router.include_router(prompts_router)
