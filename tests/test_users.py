import pytest
from httpx import AsyncClient


class TestUserProfile:
    """Tests for user profile endpoints."""

    @pytest.mark.asyncio
    async def test_get_profile_success(self, client: AsyncClient, auth_headers, test_user):
        """Test getting user profile."""
        response = await client.get("/users/profile", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"

    @pytest.mark.asyncio
    async def test_get_profile_unauthorized(self, client: AsyncClient):
        """Test getting profile without auth fails."""
        response = await client.get("/users/profile")

        assert response.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_update_profile_success(self, client: AsyncClient, auth_headers, test_user):
        """Test updating user profile."""
        response = await client.patch(
            "/users/profile", headers=auth_headers, json={"name": "Updated Name", "date_of_birth": "1990-05-15"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"

    @pytest.mark.asyncio
    async def test_update_profile_gender(self, client: AsyncClient, auth_headers, test_user):
        """Test updating profile gender."""
        response = await client.patch("/users/profile", headers=auth_headers, json={"gender": "MALE"})

        assert response.status_code == 200
        data = response.json()
        assert data["gender"] == "MALE"


class TestMyBookings:
    """Tests for user bookings endpoint."""

    @pytest.mark.asyncio
    async def test_get_my_bookings(self, client: AsyncClient, auth_headers, test_user):
        """Test getting user's bookings."""
        response = await client.get("/users/myBookings", headers=auth_headers)

        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestGuestManagement:
    """Tests for guest CRUD operations."""

    @pytest.mark.asyncio
    async def test_create_guest_success(self, client: AsyncClient, auth_headers):
        """Test creating a guest."""
        response = await client.post(
            "/users/guests", headers=auth_headers, json={"name": "New Guest", "gender": "FEMALE", "age": 25}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "New Guest"
        assert data["gender"] == "FEMALE"
        assert data["age"] == 25

    @pytest.mark.asyncio
    async def test_get_all_guests(self, client: AsyncClient, auth_headers, test_guest):
        """Test getting all guests."""
        response = await client.get("/users/guests", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    @pytest.mark.asyncio
    async def test_update_guest_success(self, client: AsyncClient, auth_headers, test_guest):
        """Test updating a guest."""
        response = await client.put(
            f"/users/guests/{test_guest.id}", headers=auth_headers, json={"name": "Updated Guest Name", "age": 35}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Guest Name"
        assert data["age"] == 35

    @pytest.mark.asyncio
    async def test_delete_guest_success(self, client: AsyncClient, auth_headers, test_guest):
        """Test deleting a guest."""
        response = await client.delete(f"/users/guests/{test_guest.id}", headers=auth_headers)

        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_delete_guest_not_found(self, client: AsyncClient, auth_headers):
        """Test deleting non-existent guest."""
        response = await client.delete("/users/guests/9999", headers=auth_headers)

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_create_guest_invalid_gender(self, client: AsyncClient, auth_headers):
        """Test creating guest with invalid gender."""
        response = await client.post(
            "/users/guests", headers=auth_headers, json={"name": "Invalid Guest", "gender": "INVALID", "age": 25}
        )

        assert response.status_code == 422
