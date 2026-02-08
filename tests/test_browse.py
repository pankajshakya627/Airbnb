import pytest
from httpx import AsyncClient
from datetime import date, timedelta


class TestHotelSearch:
    """Tests for public hotel search endpoint."""
    
    @pytest.mark.asyncio
    async def test_search_hotels_success(self, client: AsyncClient, test_hotel, test_room, db_session):
        """Test successful hotel search."""
        from app.models.inventory import Inventory
        
        # Create inventory for search
        today = date.today()
        for i in range(5):
            inv = Inventory(
                hotel_id=test_hotel.id,
                room_id=test_room.id,
                date=today + timedelta(days=i),
                book_count=0,
                reserved_count=0,
                total_count=5,
                surge_factor=1.0,
                price=199.99,
                city="Test City",
                closed=False
            )
            db_session.add(inv)
        await db_session.commit()
        
        response = await client.get("/hotels/search", params={
            "city": "Test City",
            "check_in_date": today.isoformat(),
            "check_out_date": (today + timedelta(days=4)).isoformat(),
            "rooms_count": 1
        })
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    @pytest.mark.asyncio
    async def test_search_hotels_missing_params(self, client: AsyncClient):
        """Test search with missing required parameters."""
        response = await client.get("/hotels/search")
        
        assert response.status_code == 422
    
    @pytest.mark.asyncio
    async def test_search_no_results(self, client: AsyncClient):
        """Test search with no matching hotels."""
        today = date.today()
        response = await client.get("/hotels/search", params={
            "city": "NonExistentCity",
            "check_in_date": today.isoformat(),
            "check_out_date": (today + timedelta(days=3)).isoformat(),
            "rooms_count": 1
        })
        
        assert response.status_code == 200
        assert response.json() == []


class TestHotelInfo:
    """Tests for public hotel info endpoint."""
    
    @pytest.mark.asyncio
    async def test_get_hotel_info_success(self, client: AsyncClient, test_hotel):
        """Test getting hotel info."""
        response = await client.get(f"/hotels/{test_hotel.id}/info")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Hotel"
        assert data["city"] == "Test City"
    
    @pytest.mark.asyncio
    async def test_get_hotel_info_not_found(self, client: AsyncClient):
        """Test getting non-existent hotel info."""
        response = await client.get("/hotels/9999/info")
        
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_get_inactive_hotel_info(self, client: AsyncClient, test_hotel, db_session):
        """Test that inactive hotels return 404."""
        test_hotel.active = False
        await db_session.commit()
        
        response = await client.get(f"/hotels/{test_hotel.id}/info")
        
        assert response.status_code == 404
