import pytest
from httpx import AsyncClient


class TestAuthSignup:
    """Tests for user signup endpoint."""

    @pytest.mark.asyncio
    async def test_signup_success(self, client: AsyncClient):
        """Test successful user registration."""
        response = await client.post(
            "/auth/signup", json={"email": "newuser@example.com", "password": "securepassword123", "name": "New User"}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["name"] == "New User"
        assert "GUEST" in data["roles"]
        assert "password" not in data

    @pytest.mark.asyncio
    async def test_signup_duplicate_email(self, client: AsyncClient, test_user):
        """Test signup with existing email fails."""
        response = await client.post(
            "/auth/signup",
            json={
                "email": "test@example.com",  # Already exists
                "password": "anotherpassword",
                "name": "Another User",
            },
        )

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_signup_invalid_email(self, client: AsyncClient):
        """Test signup with invalid email format."""
        response = await client.post(
            "/auth/signup", json={"email": "not-an-email", "password": "password123", "name": "Invalid User"}
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_signup_missing_fields(self, client: AsyncClient):
        """Test signup with missing required fields."""
        response = await client.post("/auth/signup", json={"email": "missing@example.com"})

        assert response.status_code == 422


class TestAuthLogin:
    """Tests for user login endpoint."""

    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient, test_user):
        """Test successful login."""
        response = await client.post("/auth/login", json={"email": "test@example.com", "password": "testpassword123"})

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["access_token"].startswith("eyJ")

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client: AsyncClient, test_user):
        """Test login with wrong password."""
        response = await client.post("/auth/login", json={"email": "test@example.com", "password": "wrongpassword"})

        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Test login with non-existent email."""
        response = await client.post(
            "/auth/login", json={"email": "nonexistent@example.com", "password": "anypassword"}
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_sets_refresh_cookie(self, client: AsyncClient, test_user):
        """Test that login sets refresh token cookie."""
        response = await client.post("/auth/login", json={"email": "test@example.com", "password": "testpassword123"})

        assert response.status_code == 200
        # Check for refresh token cookie
        assert "refreshToken" in response.cookies or "set-cookie" in response.headers


class TestAuthRefresh:
    """Tests for token refresh endpoint."""

    @pytest.mark.asyncio
    async def test_refresh_without_cookie(self, client: AsyncClient):
        """Test refresh without refresh token cookie."""
        response = await client.post("/auth/refresh")

        assert response.status_code == 401
