from fastapi import APIRouter
from starlette import status

from .submission_selectors import submission_selectors

router = APIRouter()


@router.get("/submission-selectors", status_code=status.HTTP_200_OK)
async def get_submission_selectors() -> list[str]:
    return list(submission_selectors.keys())
