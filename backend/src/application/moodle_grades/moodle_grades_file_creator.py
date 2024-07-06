import io
import csv
from collections import defaultdict

from fastapi import HTTPException

from contracts.moodle_results_data import MoodleResultsData, ProblemData, SubmissionData


class MoodleGradesFileCreator:
    def create_file(self, results_data: MoodleResultsData) -> io.StringIO:
        student_grade_map: defaultdict[str, list[float | str]] = defaultdict(lambda: [0, ''])

        file = io.StringIO()
        writer = csv.writer(file)

        contest_name = results_data.contest.name
        writer.writerow(['Email', f'{contest_name} Grade', f'{contest_name} Feedback'])

        self.mark_grades(results_data.contest.problems, student_grade_map)
        self.write_to_file(writer, student_grade_map)

        return file

    def mark_grades(self, problems: list[ProblemData], student_grade_map: defaultdict[str, list[float | str]]) -> None:
        for problem in problems:
            self.update_grades(problem, student_grade_map)

    @staticmethod
    def update_grades(problem: ProblemData, student_grade_map: defaultdict[str, list[float | str]]) -> None:
        for submission in problem.submissions:

            if submission.author_email is None:
                raise HTTPException(status_code=422, detail="Submission author email cannot be null")

            if submission.points and problem.max_points:
                problem_points = submission.points / problem.max_points * problem.max_grade
            else:
                problem_points = MoodleGradesFileCreator.get_grade_by_verdict(submission, problem)

            student_grade_map[submission.author_email][0] += problem_points

    @staticmethod
    def get_grade_by_verdict(submission: SubmissionData, problem: ProblemData) -> float:
        return problem.max_grade if submission.is_successful else 0

    @staticmethod
    def write_to_file(writer: csv.writer, student_grade_map: defaultdict[str, list[float | str]]) -> None:
        for email, (grade, feedback) in student_grade_map.items():
            writer.writerow([email, grade, feedback])
