from pydantic import BaseModel

class ProjectCreate(BaseModel):
    name: str
    description: str | None = None

class ProjectRead(BaseModel):
    id: int
    name: str
    