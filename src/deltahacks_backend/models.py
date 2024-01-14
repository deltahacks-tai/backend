from datetime import date
from typing import Self

from pydantic import BaseModel


class Announcement(BaseModel):
    title: str
    content: str
    date: date


class Assignment(BaseModel):
    name: str
    due_date: date
    description: str
    grade: int | None = None


class Course(BaseModel):
    code: str
    name: str
    professor: str
    room_number: str | None = None
    announcements: list[Announcement] = []
    assignments: list[Assignment] = []


class Courses(BaseModel):
    courses: list[Course] = []

    def get_course(self: Self, code: str) -> Course:
        for course in self.courses:
            if course.code == code:
                return course
        raise ValueError(f"Course with code {code} not found")
