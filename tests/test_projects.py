async def test_health_check(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_list_projects_empty(client):
    response = await client.get("/projects/")
    assert response.status_code == 200
    assert response.json() == []


async def test_create_project(client):
    response = await client.post("/projects/", json={"name": "Test project"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test project"
    assert "id" in data


async def test_create_project_invalid(client):
    response = await client.post("/projects/", json={})
    assert response.status_code == 422


async def test_delete_project(client):
    created = await client.post("/projects/", json={"name": "To delete"})
    project_id = created.json()["id"]

    response = await client.delete(f"/projects/{project_id}/")
    assert response.status_code == 204

    response = await client.delete(f"/projects/{project_id}/")
    assert response.status_code == 404
