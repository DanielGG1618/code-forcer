from fastapi import APIRouter

from .create_student import router as create_student_router
from .get_student import router as get_student_router
from .get_all_students import router as get_all_students_router
from .update_or_create_student import router as update_or_create_student_router
from .update_or_create_students_from_file import router as update_or_create_students_from_file_router
from .delete_student import router as delete_student_router

router = APIRouter()

router.include_router(create_student_router)
router.include_router(get_student_router)
router.include_router(get_all_students_router)
router.include_router(update_or_create_student_router)
router.include_router(update_or_create_students_from_file_router)
router.include_router(delete_student_router)
