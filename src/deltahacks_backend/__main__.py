from typing import Annotated, NamedTuple

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class Course(NamedTuple):
    name: str
    professor: str
    room_number: str | None = None


COURSES = {
    "SE 464": Course("Software Engineering", "Patrick Lam", "PG B138"),
    "CS 466": Course("Algorithms", "Jeffrey Shallit", "MC 2065"),
    "CS 488": Course("Computer Graphics", "Craig Kaplan"),
    "CS 456": Course("Computer Networks", "Ashvin Goel"),
}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.jinja2",
        context={"courses": COURSES},
    )


@app.post("/courses/{course_id}/ai", response_class=HTMLResponse)
async def course_ai(
    course_id: str,
    question: Annotated[str, Form()],
) -> str:
    return f'You asked "{question}" for {course_id}'
