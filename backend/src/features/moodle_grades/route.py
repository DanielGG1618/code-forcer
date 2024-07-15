from fastapi import APIRouter

from .create_grades_file import router as create_grades_router

router = APIRouter()

router.include_router(create_grades_router)
