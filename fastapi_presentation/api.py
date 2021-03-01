from fastapi import FastAPI

app = FastAPI(
    title="Simple API for Presentation",
    version=1.0
)

@app.get("/", tags=["Hello world API"])
def index():
    return {"Hello": "World"}