from fastapi import APIRouter

from .get_contest import router as get_contest_router
from .get_contest_results import router as get_contest_results_router

router = APIRouter()

router.include_router(get_contest_router)
router.include_router(get_contest_results_router)
