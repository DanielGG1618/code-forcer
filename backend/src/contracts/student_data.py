from pydantic import BaseModel, EmailStr


class StudentData(BaseModel):
    email: EmailStr
    handle: str
