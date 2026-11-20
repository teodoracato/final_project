from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.project import ProjectCreate, ProjectRead
from app.services import project_service

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=list[ProjectRead])
async def list_projects(session: AsyncSession = Depends(get_session)):
    return await project_service.list_projects(session)


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def add_project(data: ProjectCreate, session: AsyncSession = Depends(get_session)):
    return await project_service.create_project(session, data)


@router.delete("/{project_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, session: AsyncSession = Depends(get_session)):
    deleted = await project_service.delete_project(session, project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")