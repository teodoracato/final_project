from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.schemas.project import ProjectCreate


async def list_projects(session: AsyncSession) -> list[Project]:
    result = await session.execute(select(Project).order_by(Project.id))
    return list(result.scalars().all())


async def create_project(session: AsyncSession, data: ProjectCreate) -> Project:
    project = Project(**data.model_dump())
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


async def delete_project(session: AsyncSession, project_id: int) -> bool:
    project = await session.get(Project, project_id)
    if project is None:
        return False
    await session.delete(project)
    await session.commit()
    return True
