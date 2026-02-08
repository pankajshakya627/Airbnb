import pytest
from httpx import AsyncClient


class TestCreateRoom:
    """Tests for room creation endpoint."""
    
    @pytest.mark.asyncio
    async def test_create_room_success(self, client: AsyncClient, manager_auth_headers, test_hotel):
        """Test successful room creation."""
        response = await client.post(
            f"/admin/hotels/{test_hotel.id}/rooms",
            headers=manager_auth_headers,
            json={
                "type": "Presidential Suite",
                "base_price": 999.99,
                "photos": ["https://example.com/suite.jpg"],
                "amenities": ["king_bed", "jacuzzi", "butler_service"],
                "total_count": 2,
                "capacity": 4
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["type"] == "Presidential Suite"
        assert data["base_price"] == 999.99
        assert data["total_count"] == 2
    
    @pytest.mark.asyncio
    async def test_create_room_unauthorized(self, client: AsyncClient, test_hotel):
        """Test room creation without auth fails."""
        response = await client.post(
            f"/admin/hotels/{test_hotel.id}/rooms",
            json={
                "type": "Standard",
                "base_price": 100,
                "total_count": 5,
                "capacity": 2
            }
        )
        
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_create_room_not_owner(self, client: AsyncClient, auth_headers, test_hotel):
        """Test creating room in hotel user doesn't own."""
        response = await client.post(
            f"/admin/hotels/{test_hotel.id}/rooms",
            headers=auth_headers,
            json={
                "type": "Standard",
                "base_price": 100,
                "total_count": 5,
                "capacity": 2
            }
        )
        
        assert response.status_code == 403


class TestGetRooms:
    """Tests for listing rooms endpoint."""
    
    @pytest.mark.asyncio
    async def test_get_all_rooms(self, client: AsyncClient, manager_auth_headers, test_hotel, test_room):
        """Test getting all rooms for a hotel."""
        response = await client.get(
            f"/admin/hotels/{test_hotel.id}/rooms",
            headers=manager_auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["type"] == "Deluxe"
    
    @pytest.mark.asyncio
    async def test_get_room_by_id(self, client: AsyncClient, manager_auth_headers, test_hotel, test_room):
        """Test getting specific room."""
        response = await client.get(
            f"/admin/hotels/{test_hotel.id}/rooms/{test_room.id}",
            headers=manager_auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_room.id
        assert data["type"] == "Deluxe"


class TestUpdateRoom:
    """Tests for room update endpoint."""
    
    @pytest.mark.asyncio
    async def test_update_room_success(self, client: AsyncClient, manager_auth_headers, test_hotel, test_room):
        """Test successful room update."""
        response = await client.put(
            f"/admin/hotels/{test_hotel.id}/rooms/{test_room.id}",
            headers=manager_auth_headers,
            json={
                "base_price": 249.99,
                "total_count": 10
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["base_price"] == 249.99
        assert data["total_count"] == 10


class TestDeleteRoom:
    """Tests for room deletion endpoint."""
    
    @pytest.mark.asyncio
    async def test_delete_room_success(self, client: AsyncClient, manager_auth_headers, test_hotel, test_room):
        """Test successful room deletion."""
        response = await client.delete(
            f"/admin/hotels/{test_hotel.id}/rooms/{test_room.id}",
            headers=manager_auth_headers
        )
        
        assert response.status_code == 204
