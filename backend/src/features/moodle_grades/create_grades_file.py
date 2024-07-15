import csv
from io import StringIO
from collections import defaultdict
from datetime import datetime, timedelta

from fastapi import status, APIRouter
from fastapi.responses import StreamingResponse

from .models import MoodleResultsData, ProblemData, LateSubmissionPolicyData, SubmissionData, ContestData

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
            if submission.points and problem.max_points:
                problem_points = submission.points / problem.max_points * problem.max_grade
            else:
                problem_points = CreateGradesFileCommand._get_grade_by_verdict(submission, problem)

            problem_points = CreateGradesFileCommand._apply_late_submission_policy(results_data.late_submission_policy,
                                                                                   results_data.contest, submission,
                                                                                   problem_points)

            student_grade_map[submission.author_email][0] += problem_points

    @staticmethod
    def _get_grade_by_verdict(submission: SubmissionData, problem: ProblemData) -> float:
        return problem.max_grade if submission.is_successful else 0

    @staticmethod
    def _apply_late_submission_policy(
            late_submission_policy: LateSubmissionPolicyData,
            contest: ContestData,
            submission: SubmissionData,
            points: float
    ) -> float:

        extra_time = timedelta(seconds=late_submission_policy.extra_time)
        deadline_time = contest.start_time_utc + contest.duration
        deadline_time_extended = deadline_time + extra_time
        submission_time = submission.submission_time_utc

        if submission_time > deadline_time_extended:
            return 0.0

        if submission_time > deadline_time:
            points_deduced = points * late_submission_policy.penalty
            return points - points_deduced

        return points

    @staticmethod
    def _write_to_file(writer: csv.writer, student_grade_map: defaultdict[str, list[float | str]]) -> None:
        for email, (grade, feedback) in student_grade_map.items():
            writer.writerow([email, grade, feedback])
