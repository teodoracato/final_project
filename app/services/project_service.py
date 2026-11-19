from app.schemas.project import ProjectCreate

projects = [
    {"id": 5, "name": "webinar"},
    {"id": 2, "name": "soliter"},
]


def list_projects() -> list[dict]:
    return projects


def create_project(data: ProjectCreate) -> dict:
    ids = []
    for project in projects:
        ids.append(project["id"])

    new_id = max(ids, default=0) + 1

    new_project = {"id": new_id, "name": data.name}
    projects.append(new_project)

    return new_project


def delete_project(project_id: int) -> bool:
    for project in projects:
        if project_id == project["id"]:
            projects.remove(project)
            return True
    return False