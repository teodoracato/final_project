from fastapi import FastAPI

app = FastAPI()

projects = [
    {"id": 5, "name": "webinar"},
    {"id": 2, "name": "soliter"},
]

@app.get("/")
def health_check():
    return {"status":"ok"}

@app.get("/projects/")
def list_projects():
    return projects
