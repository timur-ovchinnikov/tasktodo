import pytest
from fastapi import status

def get_auth_headers(client, test_user):
    # Register and login
    client.post("/register", json=test_user)
    response = client.post(
        "/token",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_task(client, test_user):
    headers = get_auth_headers(client, test_user)
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "due_date": "2024-12-31T23:59:59"
    }
    response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]

def test_get_tasks(client, test_user):
    headers = get_auth_headers(client, test_user)
    # Create a task first
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "due_date": "2024-12-31T23:59:59"
    }
    client.post("/api/v1/tasks/", json=task_data, headers=headers)
    
    # Get all tasks
    response = client.get("/api/v1/tasks/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["title"] == task_data["title"]

def test_get_task_by_id(client, test_user):
    headers = get_auth_headers(client, test_user)
    # Create a task first
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "due_date": "2024-12-31T23:59:59"
    }
    create_response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
    task_id = create_response.json()["id"]
    
    # Get task by ID
    response = client.get(f"/api/v1/tasks/{task_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == task_data["title"]

def test_delete_task(client, test_user):
    headers = get_auth_headers(client, test_user)
    # Create a task first
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "due_date": "2024-12-31T23:59:59"
    }
    create_response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
    task_id = create_response.json()["id"]
    
    # Delete task
    response = client.delete(f"/api/v1/tasks/{task_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    
    # Verify task is deleted
    get_response = client.get(f"/api/v1/tasks/{task_id}", headers=headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND 