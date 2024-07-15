from __future__ import annotations

from pydantic import BaseModel, EmailStr


class Student(BaseModel):
    handle: str
    email: EmailStr | None = None

    def lower(self) -> Student:
        return Student(
            email=self.email.lower() if self.email is not None else None,
            handle=self.handle.lower()
        )

    def __hash__(self):
        return hash(self.handle)
