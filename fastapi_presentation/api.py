import time
import asyncio
import json
import aiohttp
from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(
    title="Simple API for Presentation",
    version=1.0
)

ClientSession = aiohttp.ClientSession()

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

async def get_json(client: ClientSession, url: str) -> bytes:
    async with client.get(url) as response:
        assert response.status == 200
        return await response.read()

async def get_reddit_top(subreddit: str, client: ClientSession, data: dict):
    data1 = await get_json(client, 'https://www.reddit.com/r/' + subreddit + '/top.json?sort=top&t=day&limit=5')

    j = json.loads(data1.decode('utf-8'))
    subreddit_data = []
    for i in j['data']['children']:
        score = i['data']['score']
        title = i['data']['title']
        link = i['data']['url']
        print(str(score) + ': ' + title + ' (' + link + ')')
        subreddit_data.append(str(score) + ': ' + title + ' (' + link + ')')
    data[subreddit] = subreddit_data
    print('DONE:', subreddit + '\n')


@app.get("/reddit", tags=['Asynchronous Data Fetch'])
async def get_reddit_data_api() -> dict:
    start_time: float = time.time()
    client: ClientSession = aiohttp.ClientSession()
    data: dict = {}

    await asyncio.gather(
        get_reddit_top('python', client, data),
        get_reddit_top('programming', client, data),
        get_reddit_top('compsci', client, data),
    )
    await client.close()

    print("Got reddit data in ---" + str(time.time() - start_time) + "seconds ---")
    return data