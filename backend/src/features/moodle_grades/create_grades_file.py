import csv
from io import StringIO
from collections import defaultdict
from datetime import datetime, timedelta

from fastapi import status, APIRouter
from fastapi.responses import StreamingResponse

from .models import MoodleResultsData, ProblemData, SubmissionData

router = APIRouter()


@router.post("/moodle_grades", status_code=status.HTTP_200_OK)
async def create_grades_file(results_data: MoodleResultsData) -> StreamingResponse:
    filename = f"moodle_grades_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

    file = CreateGradesFileCommand().handle(results_data)

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


class CreateGradesFileCommand:
    def handle(self, results_data: MoodleResultsData) -> StringIO:
        student_grade_map: defaultdict[str, list[float | str]] = defaultdict(lambda: [0, ''])

        file = StringIO()
        writer = csv.writer(file)

        contest_name = results_data.contest.name
        writer.writerow(['Email', f'{contest_name} Grade', f'{contest_name} Feedback'])

        self._mark_grades(results_data.contest.problems, student_grade_map, results_data)
        self._write_to_file(writer, student_grade_map)

        return file

    def _mark_grades(
            self,
            problems: list[ProblemData],
            student_grade_map: defaultdict[str, list[float | str]],
            results_data: MoodleResultsData
    ) -> None:
        for problem in problems:
            self._update_grades(problem, student_grade_map, results_data)

    @staticmethod
    def _update_grades(
            problem: ProblemData,
            student_grade_map: defaultdict[str, list[float | str]],
            results_data: MoodleResultsData
    ) -> None:
        for submission in problem.submissions:
            if submission.points is None or problem.max_points is None:
                problem_points = CreateGradesFileCommand._get_grade_by_verdict(submission, problem)
            else:
                problem_points = submission.points / problem.max_points * problem.max_grade

            problem_points = CreateGradesFileCommand._apply_late_submission_policy(results_data,
                                                                                   submission,
                                                                                   problem_points)

            student_grade_map[submission.author_email][0] += problem_points

    @staticmethod
    def _get_grade_by_verdict(submission: SubmissionData, problem: ProblemData) -> float:
        return problem.max_grade if submission.is_successful else 0

    @staticmethod
    def _apply_late_submission_policy(
            moodle_results_data: MoodleResultsData,
            submission: SubmissionData,
            points: float
    ) -> float:
        penalty = moodle_results_data.late_submission_policy.penalty
        legal_excuse = moodle_results_data.legal_excuses.get(submission.author_email)
        contest_start_time_utc = moodle_results_data.contest.start_time_utc
        contest_duration = moodle_results_data.contest.duration
        extra_time_seconds = moodle_results_data.late_submission_policy.extra_time
        submission_time = submission.submission_time_utc
        excuse_time_seconds = 0 if legal_excuse is None else legal_excuse.duration

        extra_time = timedelta(seconds=extra_time_seconds)
        excuse_time = timedelta(seconds=excuse_time_seconds)
        deadline_time = contest_start_time_utc + contest_duration + excuse_time

        deadline_time_extended = deadline_time + extra_time

        if submission_time > deadline_time_extended:
            return 0.0

        if submission_time > deadline_time:
            return points * (1 - penalty)

        return points

    @staticmethod
    def _write_to_file(writer: csv.writer, student_grade_map: defaultdict[str, list[float | str]]) -> None:
        for email, (grade, feedback) in student_grade_map.items():
            writer.writerow([email, grade, feedback])
