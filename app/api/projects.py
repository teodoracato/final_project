from fastapi import APIRouter, HTTPException, status

from app.schemas.project import ProjectCreate, ProjectRead
from app.services import project_service

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=list[ProjectRead])
def list_projects():
    return project_service.list_projects()

@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def add_project(data: ProjectCreate):
    return project_service.create_project(data)

@router.delete("/{project_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int):
    deleted = project_service.delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    