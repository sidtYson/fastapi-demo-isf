from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(
    title="Simple API for Presentation",
    version=1.0
)

class StudentSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    course_of_study: str = Field(...)
    year: int = Field(..., gt=0, lt=9)
    gpa: float = Field(..., le=4.0)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "course_of_study": "Water resources engineering",
                "year": 2,
                "gpa": 3,
            }
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


@app.get("/", tags=["Hello world API"])
def index():
    return {"Hello": "World"}

@app.post("/students", tags=["API for student data"])
def create_student(student: StudentSchema = Body(...)):
    student = jsonable_encoder(student)
    return ResponseModel(student, "Student added successfully.")