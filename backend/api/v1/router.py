from fastapi import APIRouter
from api.v1.prompts import router as prompts_router


router = APIRouter()
router.include_router(prompts_router)
