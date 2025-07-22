# tests/test_task.py

def test_login_and_get_tasks(client):
    login_response = client.post("/login", json={
        "username": "john",
        "password": "12345"
    })
    print("Login status:", login_response.status_code)
    print("Login response JSON:", login_response.get_json())

    assert login_response.status_code == 200
    data = login_response.get_json()
    token = data["access_token"]

    response = client.get("/tasks", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
