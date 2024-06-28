import io
import csv
from datetime import datetime
from typing import Dict

from contracts.moodle_results_data import MoodleResultsData, ProblemData


class MoodleGradesFileCreator:
    student_grade_map: Dict[str, list[float | str]] = {}

    def create_file(self, results_data: MoodleResultsData) -> tuple[io.StringIO, str]:
        filename = f"moodle_grades_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

        with open(filename, 'w'):
            file = io.StringIO()
            writer = csv.writer(file)
            writer.writerow(['Email', 'Grade', 'Feedback'])

            self.mark_grades(results_data.contest.problems)
            self.mark_plagiarism(results_data.plagiarizers)

            self.write_to_file(writer)

        return file, filename

    def mark_grades(self, problems: list[ProblemData]) -> None:
        for problem in problems:
            self.update_grades(problem)

    def update_grades(self, problem: ProblemData) -> None:
        for submission in problem.submissions:
            problem_points = submission.points / problem.max_points * problem.max_grade

            if self.student_grade_map.get(submission.author_email) is None:
                self.student_grade_map[submission.author_email] = [problem_points, '']
            else:
                self.student_grade_map[submission.author_email][0] += problem_points

    def mark_plagiarism(self, plagiarizers: list[str]) -> None:
        for email in plagiarizers:
            self.student_grade_map[email] = [0, 'Plagiarism detected']

    def write_to_file(self, writer: csv.writer) -> None:
        for email, response in self.student_grade_map.items():
            writer.writerow([email, response[0], response[1]])
