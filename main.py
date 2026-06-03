from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

DATA_FILE = "courses.json"


class Course(BaseModel):
    id: int
    title: str
    instructor: str
    credits: int


def load_courses():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_courses(courses):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=4)


@app.get("/")
def home():
    return {"message": "FastAPI Docker server is running"}


@app.get("/courses")
def get_courses():
    return load_courses()


@app.post("/courses")
def add_course(course: Course):
    courses = load_courses()

    for c in courses:
        if c["id"] == course.id:
            raise HTTPException(status_code=400, detail="이미 존재하는 id입니다.")

    courses.append(course.dict())
    save_courses(courses)

    return {"message": "강의가 추가되었습니다.", "course": course}