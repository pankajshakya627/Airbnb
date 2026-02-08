import pytest
from httpx import AsyncClient
from datetime import date, timedelta


class TestInventoryGet:
    """Tests for inventory retrieval endpoint."""
    
    @pytest.mark.asyncio
    async def test_get_room_inventory(self, client: AsyncClient, manager_auth_headers, test_room):
        """Test getting room inventory."""
        today = date.today()
        next_week = today + timedelta(days=7)
        
        response = await client.get(
            f"/admin/inventory/rooms/{test_room.id}",
            headers=manager_auth_headers,
            params={
                "start_date": today.isoformat(),
                "end_date": next_week.isoformat()
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    @pytest.mark.asyncio
    async def test_get_inventory_unauthorized(self, client: AsyncClient, test_room):
        """Test getting inventory without auth fails."""
        response = await client.get(f"/admin/inventory/rooms/{test_room.id}")
        
        assert response.status_code == 401


class TestInventoryUpdate:
    """Tests for inventory update endpoint."""
    
    @pytest.mark.asyncio
    async def test_update_inventory_surge_factor(self, client: AsyncClient, manager_auth_headers, test_room, db_session):
        """Test updating surge factor."""
        from app.models.inventory import Inventory
        
        # Create inventory for room
        today = date.today()
        inventory = Inventory(
            hotel_id=test_room.hotel_id,
            room_id=test_room.id,
            date=today,
            book_count=0,
            reserved_count=0,
            total_count=5,
            surge_factor=1.0,
            price=199.99,
            city="Test City",
            closed=False
        )
        db_session.add(inventory)
        await db_session.commit()
        
        response = await client.patch(
            f"/admin/inventory/rooms/{test_room.id}",
            headers=manager_auth_headers,
            params={
                "start_date": today.isoformat(),
                "end_date": today.isoformat()
            },
            json={
                "surge_factor": 1.5,
                "price": 299.99
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        if len(data) > 0:
            assert data[0]["surge_factor"] == 1.5
            assert data[0]["price"] == 299.99
    
    @pytest.mark.asyncio
    async def test_close_inventory(self, client: AsyncClient, manager_auth_headers, test_room, db_session):
        """Test closing inventory (marking room unavailable)."""
        from app.models.inventory import Inventory
        
        today = date.today()
        inventory = Inventory(
            hotel_id=test_room.hotel_id,
            room_id=test_room.id,
            date=today,
            book_count=0,
            reserved_count=0,
            total_count=5,
            surge_factor=1.0,
            price=199.99,
            city="Test City",
            closed=False
        )
        db_session.add(inventory)
        await db_session.commit()
        
        response = await client.patch(
            f"/admin/inventory/rooms/{test_room.id}",
            headers=manager_auth_headers,
            params={"start_date": today.isoformat()},
            json={"closed": True}
        )
        
        assert response.status_code == 200
