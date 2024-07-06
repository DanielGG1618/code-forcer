from fastapi import FastAPI, UploadFile, File, status
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse

from datetime import datetime

from application.contests.contests_service import ContestsService
from application.moodle_grades.moodle_grades_file_creator import MoodleGradesFileCreator
from application.students.students_service import StudentsService
from contracts.moodle_results_data import MoodleResultsData
from domain.contest import Contest
from domain.student import Student
from contracts.student_data import StudentData
from container import container

app = FastAPI()

origins = [
    "https://mashfeii.ru",
    "http://codeforcer.mashfeii.com",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc)},
    )


@app.post("/students", status_code=status.HTTP_201_CREATED)
async def create_student(student_data: StudentData) -> Student | None:
    return container[StudentsService].create_student(student_data)


@app.post("/students/file", status_code=status.HTTP_201_CREATED)
async def create_students_from_file(file: UploadFile = File(...)) -> list[Student]:
    return container[StudentsService].create_students_from_file(file)


@app.get("/students/{email_or_handle}", status_code=status.HTTP_200_OK)
async def get_student_by_email_or_handle(email_or_handle: str) -> Student:
    return container[StudentsService].get_student_by_email_or_handle(email_or_handle)


@app.put("/students/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def update_student(email: str, updated_student_data: StudentData) -> None:
    container[StudentsService].update_student(email, updated_student_data)


@app.delete("/students/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(email: str) -> None:
    container[StudentsService].delete_student(email)


@app.get("/contests/{contest_id}/results", status_code=status.HTTP_200_OK)
async def get_results(contest_id: int, key: str, secret: str):
    return container[ContestsService].get_contest_results(contest_id, key, secret)


@app.get("/contests/{contest_id}", status_code=status.HTTP_200_OK)
async def get_contest(contest_id: int, key: str, secret: str) -> Contest:
    return container[ContestsService].get_contest(contest_id, key, secret)


@app.post("/moodle_grades", status_code=status.HTTP_200_OK)
async def get_grades(results_data: MoodleResultsData) -> StreamingResponse:
    filename = f"moodle_grades_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    file = container[MoodleGradesFileCreator].create_file(results_data)
    content_length = len(file.getvalue())
    file.seek(0)

    return StreamingResponse(
        file,
        headers={
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Content-Type': 'text/csv; charset=utf-8',
            'Content-Length': str(content_length),
        },
        media_type='text/csv'
    )


if __name__ == '__main__':
    run(app, host='127.0.0.1', port=8000)
