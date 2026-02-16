import pytest
from httpx import AsyncClient


class TestCreateHotel:
    """Tests for hotel creation endpoint."""

    @pytest.mark.asyncio
    async def test_create_hotel_success(self, client: AsyncClient, manager_auth_headers):
        """Test successful hotel creation."""
        response = await client.post(
            "/admin/hotels",
            headers=manager_auth_headers,
            json={
                "name": "Luxury Resort",
                "city": "Miami",
                "photos": ["https://example.com/photo1.jpg"],
                "amenities": ["wifi", "pool", "spa"],
                "contact_info": {"phone": "+1-555-0100", "email": "contact@luxury.com", "address": "100 Beach Blvd"},
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Luxury Resort"
        assert data["city"] == "Miami"
        assert data["active"] is False

    @pytest.mark.asyncio
    async def test_create_hotel_unauthorized(self, client: AsyncClient):
        """Test hotel creation without auth fails."""
        response = await client.post("/admin/hotels", json={"name": "Test Hotel", "city": "NYC"})

        assert response.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_create_hotel_guest_forbidden(self, client: AsyncClient, auth_headers):
        """Test guest cannot create hotel."""
        response = await client.post("/admin/hotels", headers=auth_headers, json={"name": "Guest Hotel", "city": "LA"})

        assert response.status_code == 403


class TestGetHotels:
    """Tests for listing hotels endpoint."""

    @pytest.mark.asyncio
    async def test_get_hotels_success(self, client: AsyncClient, manager_auth_headers, test_hotel):
        """Test getting owned hotels."""
        response = await client.get("/admin/hotels", headers=manager_auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["name"] == "Test Hotel"

    @pytest.mark.asyncio
    async def test_get_hotel_by_id(self, client: AsyncClient, manager_auth_headers, test_hotel):
        """Test getting hotel by ID."""
        response = await client.get(f"/admin/hotels/{test_hotel.id}", headers=manager_auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_hotel.id
        assert data["name"] == "Test Hotel"

    @pytest.mark.asyncio
    async def test_get_hotel_not_found(self, client: AsyncClient, manager_auth_headers):
        """Test getting non-existent hotel."""
        response = await client.get("/admin/hotels/9999", headers=manager_auth_headers)

        assert response.status_code == 404


class TestUpdateHotel:
    """Tests for hotel update endpoint."""

    @pytest.mark.asyncio
    async def test_update_hotel_success(self, client: AsyncClient, manager_auth_headers, test_hotel):
        """Test successful hotel update."""
        response = await client.put(
            f"/admin/hotels/{test_hotel.id}",
            headers=manager_auth_headers,
            json={"name": "Updated Hotel Name", "amenities": ["wifi", "pool", "gym", "spa"]},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Hotel Name"
        assert "spa" in data["amenities"]

    @pytest.mark.asyncio
    async def test_update_hotel_not_owner(self, client: AsyncClient, auth_headers, test_hotel):
        """Test updating hotel by non-owner fails."""
        response = await client.put(
            f"/admin/hotels/{test_hotel.id}", headers=auth_headers, json={"name": "Hacked Hotel"}
        )

        assert response.status_code == 403


class TestActivateHotel:
    """Tests for hotel activation endpoint."""

    @pytest.mark.asyncio
    async def test_activate_hotel_success(self, client: AsyncClient, manager_auth_headers, test_hotel, db_session):
        """Test successful hotel activation."""
        # First set hotel to inactive
        test_hotel.active = False
        await db_session.commit()

        response = await client.patch(f"/admin/hotels/{test_hotel.id}/activate", headers=manager_auth_headers)

        assert response.status_code == 204


class TestDeleteHotel:
    """Tests for hotel deletion endpoint."""

    @pytest.mark.asyncio
    async def test_delete_hotel_success(self, client: AsyncClient, manager_auth_headers, test_hotel):
        """Test successful hotel deletion."""
        response = await client.delete(f"/admin/hotels/{test_hotel.id}", headers=manager_auth_headers)

        assert response.status_code == 204

        # Verify deletion
        response = await client.get(f"/admin/hotels/{test_hotel.id}", headers=manager_auth_headers)
        assert response.status_code == 404


class TestHotelReports:
    """Tests for hotel reports endpoint."""

    @pytest.mark.asyncio
    async def test_get_hotel_bookings(self, client: AsyncClient, manager_auth_headers, test_hotel):
        """Test getting hotel bookings."""
        response = await client.get(f"/admin/hotels/{test_hotel.id}/bookings", headers=manager_auth_headers)

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @pytest.mark.asyncio
    async def test_get_hotel_report(self, client: AsyncClient, manager_auth_headers, test_hotel):
        """Test getting hotel report."""
        response = await client.get(
            f"/admin/hotels/{test_hotel.id}/reports",
            headers=manager_auth_headers,
            params={"start_date": "2026-01-01", "end_date": "2026-12-31"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "total_bookings" in data
        assert "total_revenue" in data
