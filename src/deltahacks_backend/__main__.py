import os
from contextlib import asynccontextmanager
from datetime import date
from typing import Annotated, AsyncGenerator
from uuid import uuid4

from cohere.client_async import AsyncClient
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .models import Announcement, Assignment, Course, Courses

co = AsyncClient(os.environ["COHERE_API_KEY"])


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield
    await co.close()


COURSES = Courses(
    courses=[
        Course(
            code="CS 101",
            name="Introduction to Programming",
            professor="Dr. Emily Johnson",
            room_number="EN 2001",
            announcements=[
                Announcement(
                    title="Welcome to CS 101!",
                    content="I am thrilled to welcome you all to the Introduction to Programming course. Over the semester, we will embark on a fascinating journey to grasp fundamental programming concepts using the versatile Python language. As we dive into the world of coding, I encourage you to actively participate in class discussions and engage in hands-on programming exercises.",
                    date=date(2024, 1, 15),
                ),
                Announcement(
                    title="Programming Environment Setup",
                    content="To ensure a smooth start, make sure to install Python and set up your development environment before our first class on January 25th. If you encounter any challenges, don't hesitate to reach out during my office hours for assistance.",
                    date=date(2024, 1, 18),
                ),
            ],
            assignments=[
                Assignment(
                    name="Hello World Program",
                    due_date=date(2024, 1, 30),
                    description="Your first assignment is to write a simple 'Hello, World!' program in Python. This foundational task will set the stage for our subsequent coding adventures.",
                ),
                Assignment(
                    name="Calculator App",
                    due_date=date(2024, 2, 10),
                    description="For our second assignment, let's delve into application development. Your task is to create a basic calculator application with addition, subtraction, multiplication, and division functionalities. This project will reinforce your programming skills and provide practical experience in building useful software.",
                ),
            ],
        ),
        Course(
            code="ENG 202",
            name="World Literature",
            professor="Dr. Maria Rodriguez",
            room_number="LIB 3003",
            announcements=[
                Announcement(
                    title="Welcome to World Literature!",
                    content="Greetings, literature enthusiasts! In this captivating course, we will explore the rich tapestry of world literature, spanning ancient epics to modern masterpieces. Prepare yourselves for an exciting intellectual journey filled with insightful discussions and literary discoveries.",
                    date=date(2024, 1, 15),
                ),
                Announcement(
                    title="Reading List",
                    content="Our first assignment is an enthralling one – read 'One Hundred Years of Solitude' by Gabriel Garcia Marquez. As we gather for our next class on January 28th, be ready to engage in a thought-provoking discussion about the intricate themes and characters woven into this literary masterpiece.",
                    date=date(2024, 1, 22),
                ),
            ],
            assignments=[
                Assignment(
                    name="Literary Analysis Essay",
                    due_date=date(2024, 2, 15),
                    description="For your first assignment, you will embark on a literary exploration. You are to write a compelling literary analysis essay on a selected work from the reading list, delving into themes, characters, and symbolism. This assignment aims to sharpen your analytical skills and deepen your appreciation for the nuances of literature.",
                ),
                Assignment(
                    name="Creative Writing Project",
                    due_date=date(2024, 3, 5),
                    description="Get ready to unleash your creative spirit! Your second assignment is to create an original short story inspired by the literary styles and themes encountered throughout the course. This project encourages you to experiment with narrative techniques and express your unique voice in the realm of creative writing.",
                ),
            ],
        ),
        Course(
            code="PHY 301",
            name="Advanced Quantum Mechanics",
            professor="Dr. Michael Chen",
            room_number="SCI 4010",
            announcements=[
                Announcement(
                    title="Welcome to PHY 301!",
                    content="Welcome, future quantum physicists! This course promises a mind-expanding exploration of advanced quantum mechanics. Get ready to unravel the mysteries of the quantum world through engaging lectures, stimulating discussions, and hands-on experiments.",
                    date=date(2024, 1, 15),
                ),
                Announcement(
                    title="Lab Sessions",
                    content="Exciting times ahead! Our first lab session is scheduled for January 30th. Ensure you have your lab notebooks and safety gear ready as we delve into practical experiments that complement the theoretical aspects of quantum mechanics.",
                    date=date(2024, 1, 25),
                ),
            ],
            assignments=[
                Assignment(
                    name="Quantum Entanglement Research Paper",
                    due_date=date(2024, 2, 20),
                    description="Prepare to dive deep into the realm of quantum phenomena. Your first assignment is to conduct research on quantum entanglement and submit a comprehensive research paper discussing its implications and applications. This project aims to enhance your understanding of cutting-edge quantum concepts and their real-world significance.",
                ),
                Assignment(
                    name="Wave Function Simulation",
                    due_date=date(2024, 3, 10),
                    description="Put your theoretical knowledge into action! For your second assignment, develop a computer simulation illustrating the behavior of wave functions in quantum systems. This hands-on project will provide valuable insights into the practical applications of advanced quantum mechanics.",
                ),
            ],
        ),
        Course(
            code="ART 150",
            name="Introduction to Digital Art",
            professor="Prof. Sarah Thompson",
            room_number="ART 102",
            announcements=[
                Announcement(
                    title="Welcome to ART 150!",
                    content="Greetings, budding digital artists! This course is your gateway to the vibrant world of digital art. Get ready to unleash your creativity using digital tools and techniques, exploring the boundless possibilities of visual expression.",
                    date=date(2024, 1, 16),
                ),
                Announcement(
                    title="Digital Art Exhibition",
                    content="Exciting news! As part of our creative journey, we will organize a digital art exhibition showcasing your projects. Start brainstorming ideas for your unique digital art piece that will be featured in this exhibition, providing you with a platform to showcase your artistic talent.",
                    date=date(2024, 1, 23),
                ),
            ],
            assignments=[
                Assignment(
                    name="Digital Self-Portrait",
                    due_date=date(2024, 2, 5),
                    description="Embark on your artistic journey with your first assignment – to create a digital self-portrait using graphic design software. Experiment with different styles and techniques to capture your unique personality and artistic vision.",
                ),
                Assignment(
                    name="Animated Digital Artwork",
                    due_date=date(2024, 3, 1),
                    description="Venture into the dynamic realm of digital storytelling! Your second assignment challenges you to produce an animated digital artwork, experimenting with motion and visual storytelling. This project encourages you to push the boundaries of digital art and explore the fusion of technology and creativity.",
                ),
            ],
        ),
    ]
)


def kebab(s: str) -> str:
    return s.replace(" ", "").lower()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


templates.env.filters["kebab"] = kebab  # type: ignore


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.jinja2",
        context={"courses": COURSES},
    )


@app.get("/courses/{course_code}", response_class=HTMLResponse)
async def course(request: Request, course_code: str) -> HTMLResponse:
    conversation_id = uuid4()
    return templates.TemplateResponse(
        request=request,
        name="course.jinja2",
        context={
            "course": COURSES.get_course(course_code),
            "conversation_id": conversation_id,
        },
    )


@app.post("/chat", response_class=HTMLResponse)
async def chat(
    request: Request,
    conversation_id: Annotated[str, Form()],
    message: Annotated[str, Form()],
) -> HTMLResponse:
    response = await co.chat(
        message,
        preamble_override="You are a bot which replies to answers as concisely as possible. Do not use more than once sentence in a response under ANY cirumstances.",
        max_tokens=50,
        conversation_id=conversation_id,
    )

    return templates.TemplateResponse(
        request=request,
        name="components/chat-message.jinja2",
        context={"user_message": message, "bot_message": response.text},
    )


@app.post("/courses/{course_code}/ai", response_class=HTMLResponse)
async def course_ai(
    course_code: str,
    question: Annotated[str, Form()],
) -> str:
    course = COURSES.get_course(course_code)

    documents = list[str]()

    documents.append(f"The course name is {course.name}.")
    documents.append(f"The course code is {course.code}.")
    documents.append(f"The professor for is {course.professor}.")

    if course.room_number:
        documents.append(f"The room number is {course.room_number}.")
    else:
        documents.append("The course is online.")

    for announcement in course.announcements:
        documents.append(
            f'The announcement "{announcement.title}" was made on {announcement.date}.'
        )
        documents.append(
            f'The announcement "{announcement.title}" is about {announcement.content}.'
        )

    for assignment in course.assignments:
        documents.append(
            f'The assignment "{assignment.name}" is due on {assignment.due_date}.'
        )
        documents.append(
            f'The description for the assignment "{assignment.name}" is: {assignment.description}.'
        )
        if assignment.grade:
            documents.append(
                f'You got a grade of {assignment.grade} on the assignment "{assignment.name}".'
            )

    reranking = await co.rerank(
        question,
        model="rerank-english-v2.0",
        documents=documents,
        top_n=1,
    )

    relevance_score = reranking.results[0].relevance_score

    if relevance_score < 0.85:
        return "Sorry, I don't understand your question."

    return reranking.results[0].document["text"]
