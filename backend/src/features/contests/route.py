from fastapi import APIRouter

from .get_contest import router as get_contest_router

router = APIRouter()

router.include_router(get_contest_router)
