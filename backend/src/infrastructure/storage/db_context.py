import sqlite3

from src.utils.singleton_meta import SingletonMeta


class DBContext(metaclass=SingletonMeta):
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

        self.__ensure_students_db_is_created()

    def commit(self) -> None:
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()

    def execute_command(self, command: str, parameters=()) -> sqlite3.Cursor:
        return self.cursor.execute(command, parameters)

    def __ensure_students_db_is_created(self) -> None:
        self.execute_command("""
            CREATE TABLE IF NOT EXISTS students (
                email TEXT PRIMARY KEY,
                handle TEXT
            );
        """)
        self.commit()
