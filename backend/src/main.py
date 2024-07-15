from fastapi import FastAPI
from fastapi.responses import JSONResponse
from uvicorn import run
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.features.students.route import router as students_router
from src.features.contests.route import router as contests_router
from src.features.moodle_grades.route import router as moodle_grades_router

app = FastAPI()
app.include_router(students_router)
app.include_router(contests_router)
app.include_router(moodle_grades_router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc)},
    )


if __name__ == '__main__':
    run(app, host='127.0.0.1', port=8000)
