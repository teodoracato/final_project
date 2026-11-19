from fastapi import APIRouter

router = APIRouter(prefix="/projects", tags=["projects"])

projects = [
    {"id": 5, "name": "webinar"},
    {"id": 2, "name": "soliter"},
]


@router.get("/")
def list_projects():
    return projects