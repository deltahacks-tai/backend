import os
from typing import Annotated, NamedTuple

from cohere.client import Client
from cohere.responses.classify import Example
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def kebab(s: str) -> str:
    return s.replace(" ", "").lower()


templates.env.filters["kebab"] = kebab  # pyright: ignore[reportUnknownMemberType]


class Course(NamedTuple):
    name: str
    professor: str
    room_number: str | None = None
    assignments: dict[str, int] = {}


COURSES = {
    "SE 464": Course(
        "Software Engineering",
        "Patrick Lam",
        "PG B138",
        {
            "Create a Graph Search Algorithm": 2,
            "SQL Injection Defense": 3,
        },
    ),
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


@app.get("/course/{course_id}", response_class=HTMLResponse)
async def course(request: Request, course_id: str) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="course.jinja2")


co = Client(os.environ["COHERE_API_KEY"])


@app.post("/courses/{course_id}/ai", response_class=HTMLResponse)
async def course_ai(
    course_id: str,
    question: Annotated[str, Form()],
) -> str:
    examples = list[Example]()

    for assignment in COURSES[course_id].assignments:
        examples.append(
            Example(f"How many days until {assignment} is due?", assignment)
        )
        examples.append(Example(f"When is {assignment} due?", assignment))
        examples.append(Example(f"When should I submit {assignment}?", assignment))

    classifications = co.classify(
        [question],
        examples=examples,
    )

    prediction = classifications.classifications[0].prediction
    confidence = classifications.classifications[0].confidence

    if prediction is None or confidence is None:
        return "I don't understand the question"

    return f"the assignment is due in {COURSES[course_id].assignments[prediction]} days [{confidence:.2f}]"
