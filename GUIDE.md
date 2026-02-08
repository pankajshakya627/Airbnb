# AirBnb API Complete Guide

This guide walks you through all API endpoints step-by-step with working examples.

---

## Table of Contents

1. [Quick Setup](#quick-setup)
2. [Authentication](#authentication)
3. [Upgrade to Hotel Manager](#upgrade-to-hotel-manager)
4. [User Profile](#user-profile)
5. [Guest Management](#guest-management)
6. [Hotel Management (Admin)](#hotel-management-admin)
7. [Room Management (Admin)](#room-management-admin)
8. [Inventory Management (Admin)](#inventory-management-admin)
9. [Hotel Browse (Public)](#hotel-browse-public)
10. [Booking Flow](#booking-flow)

---

## Quick Setup

**Set these variables in your terminal (no spaces around =):**

```bash
export BASE_URL="http://localhost:8000"
```

**After login, set your token (no spaces around =):**

```bash
# ✅ Correct
export TOKEN="your_access_token_here"

# ❌ Wrong - spaces cause "bad assignment" error
export TOKEN = "your_token"
```

---

## Authentication

### 1. Signup - Create Account

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass123",
    "name": "John Doe"
  }'
```

**Success Response:**

```json
{
  "id": 1,
  "email": "john@example.com",
  "name": "John Doe",
  "date_of_birth": null,
  "gender": null,
  "roles": ["GUEST"]
}
```

**Error Response (Email exists):**

```json
{ "detail": "Email already registered" }
```

### 2. Login - Get Token

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**⚠️ IMPORTANT: Save the token (no spaces around =):**

```bash
export TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sZXMiOlsiR1VFU1QiLCJIT1RFTF9NQU5BR0VSIl0sImV4cCI6MTc3MDU1MTExMSwidHlwZSI6ImFjY2VzcyJ9.Ud7fTyjmV9YKPwBYHw0hSIBnb5AcTQhgW9TduGoZJIc"
```

### 3. Refresh Token

```bash
curl -X POST http://localhost:8000/auth/refresh \
  --cookie "refreshToken=your_refresh_token"
```

---

## Upgrade to Hotel Manager

By default, new users have only `GUEST` role. To manage hotels, you need `HOTEL_MANAGER` role.

### Step 1: Add HOTEL_MANAGER Role via SQL

```bash
psql -d airbnb -c "UPDATE app_user SET roles = '{GUEST,HOTEL_MANAGER}' WHERE email = 'john@example.com';"
```

**Output:**

```
UPDATE 1
```

### Step 2: Login Again to Get New Token

After updating roles, you MUST login again to get a token with the new role:

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "securepass123"}'
```

**Response (notice HOTEL_MANAGER in roles):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sZXMiOlsiR1VFU1QiLCJIT1RFTF9NQU5BR0VSIl0...",
  "token_type": "bearer"
}
```

### Step 3: Update TOKEN Variable

```bash
export TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sZXMiOlsiR1VFU1QiLCJIT1RFTF9NQU5BR0VSIl0sImV4cCI6MTc3MDU1MTExMSwidHlwZSI6ImFjY2VzcyJ9.Ud7fTyjmV9YKPwBYHw0hSIBnb5AcTQhgW9TduGoZJIc"
```

**Available Roles:**
| Role | Permissions |
|------|-------------|
| `GUEST` | Browse hotels, make bookings |
| `HOTEL_MANAGER` | Create/manage hotels, rooms, inventory |

---

## User Profile

### 4. Get Profile

```bash
curl -X GET http://localhost:8000/users/profile \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**

```json
{
  "id": 1,
  "email": "john@example.com",
  "name": "John Doe",
  "date_of_birth": null,
  "gender": null,
  "roles": ["GUEST", "HOTEL_MANAGER"]
}
```

### 5. Update Profile

```bash
curl -X PATCH http://localhost:8000/users/profile \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "date_of_birth": "1990-05-15",
    "gender": "MALE"
  }'
```

### 6. Get My Bookings

```bash
curl -X GET http://localhost:8000/users/myBookings \
  -H "Authorization: Bearer $TOKEN"
```

---

## Guest Management

### 7. Create Guest

```bash
curl -X POST http://localhost:8000/users/guests \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Guest Name",
    "gender": "FEMALE",
    "age": 28
  }'
```

### 8. Get All Guests

```bash
curl -X GET http://localhost:8000/users/guests \
  -H "Authorization: Bearer $TOKEN"
```

### 9. Update Guest

```bash
curl -X PUT http://localhost:8000/users/guests/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Guest",
    "age": 30
  }'
```

### 10. Delete Guest

```bash
curl -X DELETE http://localhost:8000/users/guests/1 \
  -H "Authorization: Bearer $TOKEN"
```

---

## Hotel Management (Admin)

**⚠️ Requires HOTEL_MANAGER role** (see [Upgrade to Hotel Manager](#upgrade-to-hotel-manager))

### 11. Create Hotel

```bash
curl -X POST http://localhost:8000/admin/hotels \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Grand Hotel",
    "city": "New York",
    "photos": ["https://example.com/photo1.jpg"],
    "amenities": ["wifi", "pool", "gym"],
    "contact_info": {
      "phone": "+1-555-0100",
      "email": "hotel@example.com",
      "address": "123 Main St, New York"
    }
  }'
```

### 12. Get All My Hotels

```bash
curl -X GET http://localhost:8000/admin/hotels \
  -H "Authorization: Bearer $TOKEN"
```

### 13. Get Hotel by ID

```bash
curl -X GET http://localhost:8000/admin/hotels/1 \
  -H "Authorization: Bearer $TOKEN"
```

### 14. Update Hotel

```bash
curl -X PUT http://localhost:8000/admin/hotels/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Grand Hotel NYC",
    "amenities": ["wifi", "pool", "gym", "spa"]
  }'
```

### 15. Activate Hotel

```bash
curl -X PATCH http://localhost:8000/admin/hotels/1/activate \
  -H "Authorization: Bearer $TOKEN"
```

### 16. Delete Hotel

```bash
curl -X DELETE http://localhost:8000/admin/hotels/1 \
  -H "Authorization: Bearer $TOKEN"
```

### 17. Get Hotel Bookings

```bash
curl -X GET http://localhost:8000/admin/hotels/1/bookings \
  -H "Authorization: Bearer $TOKEN"
```

### 18. Get Hotel Report

```bash
curl -X GET "http://localhost:8000/admin/hotels/1/reports?start_date=2026-01-01&end_date=2026-12-31" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Room Management (Admin)

### 19. Create Room

```bash
curl -X POST http://localhost:8000/admin/hotels/1/rooms \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Deluxe Suite",
    "base_price": 299.99,
    "photos": ["https://example.com/room.jpg"],
    "amenities": ["king_bed", "balcony", "minibar"],
    "total_count": 10,
    "capacity": 2
  }'
```

### 20. Get All Rooms

```bash
curl -X GET http://localhost:8000/admin/hotels/1/rooms \
  -H "Authorization: Bearer $TOKEN"
```

### 21. Get Room by ID

```bash
curl -X GET http://localhost:8000/admin/hotels/1/rooms/1 \
  -H "Authorization: Bearer $TOKEN"
```

### 22. Update Room

```bash
curl -X PUT http://localhost:8000/admin/hotels/1/rooms/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "base_price": 349.99,
    "total_count": 15
  }'
```

### 23. Delete Room

```bash
curl -X DELETE http://localhost:8000/admin/hotels/1/rooms/1 \
  -H "Authorization: Bearer $TOKEN"
```

---

## Inventory Management (Admin)

### 24. Get Room Inventory

```bash
curl -X GET "http://localhost:8000/admin/inventory/rooms/1?start_date=2026-02-01&end_date=2026-02-28" \
  -H "Authorization: Bearer $TOKEN"
```

### 25. Update Inventory

```bash
curl -X PATCH "http://localhost:8000/admin/inventory/rooms/1?start_date=2026-02-14&end_date=2026-02-16" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "surge_factor": 1.5,
    "price": 449.99,
    "closed": false
  }'
```

---

## Hotel Browse (Public)

### 26. Search Hotels

```bash
curl -X GET "http://localhost:8000/hotels/search?city=New%20York&check_in_date=2026-03-01&check_out_date=2026-03-05&rooms_count=1"
```

### 27. Get Hotel Info

```bash
curl -X GET http://localhost:8000/hotels/1/info
```

---

## Booking Flow

### 28. Initialize Booking

```bash
curl -X POST http://localhost:8000/bookings/init \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "hotel_id": 1,
    "room_id": 1,
    "check_in_date": "2026-03-01",
    "check_out_date": "2026-03-05",
    "rooms_count": 1
  }'
```

**Response:**

```json
{
  "id": 1,
  "hotel_id": 1,
  "room_id": 1,
  "booking_status": "RESERVED",
  "amount": 1199.96
}
```

### 29. Add Guests to Booking

```bash
curl -X POST http://localhost:8000/bookings/1/addGuests \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '[1, 2]'
```

### 30. Initiate Payment

```bash
curl -X POST http://localhost:8000/bookings/1/payments \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**

```json
{ "session_url": "https://checkout.stripe.com/pay/cs_test_..." }
```

### 31. Check Booking Status

```bash
curl -X GET http://localhost:8000/bookings/1/status \
  -H "Authorization: Bearer $TOKEN"
```

### 32. Cancel Booking

```bash
curl -X POST http://localhost:8000/bookings/1/cancel \
  -H "Authorization: Bearer $TOKEN"
```

---

## Quick Reference

### Working Test Credentials

```
Email: john@example.com
Password: securepass123
Roles: GUEST, HOTEL_MANAGER
```

### Token Expiration

- Access Token: 30 minutes
- Refresh Token: 7 days

### Booking Status Flow

```
RESERVED → GUESTS_ADDED → PAYMENTS_PENDING → CONFIRMED
                                          ↘ CANCELLED
```

### Gender Values

- `MALE`
- `FEMALE`

### Swagger UI

Open **http://localhost:8000/docs** for interactive testing!
