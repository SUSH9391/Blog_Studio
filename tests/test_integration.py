import pytest
from main import app
from routers.users import OAuth2PasswordRequestForm

@pytest.mark.anyio
async def test_homepage_renders(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert "Home" in response.text
    assert '<article class="reddit-card"' in response.text  # Posts container

@pytest.mark.anyio
async def test_login_page_renders(client):
    response = await client.get("/login")
    assert response.status_code == 200
    assert 'name="username"' in response.text
    assert 'name="password"' in response.text

@pytest.mark.anyio
async def test_login_success(client, seeded_user):
    form_data = {
        "username": "sushmitha@example.com",  # or "sushmitha" if username-based
        "password": "abc123@$"
    }
    response = await client.post("/api/users/token", data=form_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.anyio
async def test_login_failure(client):
    form_data = {"username": "wrong@example.com", "password": "wrong"}
    response = await client.post("/api/users/token", data=form_data)
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

@pytest.mark.anyio
async def test_account_protected_no_token(client):
    response = await client.get("/account")
    assert response.status_code == 200  # Renders template, but JS redirects

# Note: Full protected API test would need token in headers
