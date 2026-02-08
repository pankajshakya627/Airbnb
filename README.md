# AirBnb FastAPI Backend

## 🏨 Project Overview

A robust, production-ready Hotel Management & Booking System backend built with **FastAPI**. This project is a complete conversion of a legacy Spring Boot application to a modern, high-performance Python architecture. It features secure authentication, role-based access control, comprehensive booking flows, and Stripe payment integration.

## ✨ Key Features

- **Authentication & Security**: JWT-based auth, BCrypt password hashing, and Role-Based Access Control (RBAC) for Guests and Hotel Managers.
- **Hotel Management**: Complete CRUD for Hotels, Rooms, and Amenities.
- **Dynamic Inventory**: Intelligent room inventory management with surge pricing capabilities.
- **Booking Engine**: Full booking lifecycle management (Reservation -> Payment -> Confirmation -> Cancellation).
- **Payment Integration**: Seamless Stripe checkout integration with webhook handling.
- **Search & Filtering**: Optimized search functionality for finding available hotels by city and dates.
- **Database Migrations**: Automated schema management using Alembic.
- **Dockerized**: Fully containerized setup for easy deployment.

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 14+
- **ORM**: SQLAlchemy (Async)
- **Migrations**: Alembic
- **Validation**: Pydantic
- **Testing**: Pytest & HTTPX
- **Payments**: Stripe API
- **Containerization**: Docker & Docker Compose

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 14+

### Setup

```bash
# Clone and navigate
cd /Volumes/CrucialX9_MAC/github_repos/AirBnbfastapi

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure database
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

**Access the API:**

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📚 API Reference & Examples

### Authentication

#### 1. User Signup

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass123",
    "name": "John Doe"
  }'
```

**Response:**

```json
{
  "id": 1,
  "email": "john@example.com",
  "name": "John Doe",
  "roles": ["GUEST"]
}
```

#### 2. User Login

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
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 3. Refresh Token

```bash
curl -X POST http://localhost:8000/auth/refresh \
  --cookie "refreshToken=your_refresh_token"
```

---

### Hotel Management (Admin)

> **Note:** All admin endpoints require `HOTEL_MANAGER` role.

#### 4. Create Hotel

```bash
curl -X POST http://localhost:8000/admin/hotels \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Grand Hyatt",
    "city": "New York",
    "photos": ["https://example.com/photo1.jpg"],
    "amenities": ["wifi", "pool", "gym"],
    "contact_info": {
      "phone": "+1-555-0100",
      "email": "contact@grandhyatt.com",
      "address": "109 E 42nd St, New York"
    }
  }'
```

#### 5. Get All Hotels

```bash
curl -X GET http://localhost:8000/admin/hotels \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 6. Update Hotel

```bash
curl -X PUT http://localhost:8000/admin/hotels/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Grand Hyatt NYC",
    "amenities": ["wifi", "pool", "gym", "spa"]
  }'
```

#### 7. Activate Hotel

```bash
curl -X PATCH http://localhost:8000/admin/hotels/1/activate \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 8. Delete Hotel

```bash
curl -X DELETE http://localhost:8000/admin/hotels/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### Room Management (Admin)

#### 9. Create Room

```bash
curl -X POST http://localhost:8000/admin/hotels/1/rooms \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Deluxe Suite",
    "base_price": 299.99,
    "photos": ["https://example.com/room1.jpg"],
    "amenities": ["king_bed", "balcony", "minibar"],
    "total_count": 10,
    "capacity": 2
  }'
```

#### 10. Get All Rooms

```bash
curl -X GET http://localhost:8000/admin/hotels/1/rooms \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 11. Update Room

```bash
curl -X PUT http://localhost:8000/admin/hotels/1/rooms/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "base_price": 349.99,
    "total_count": 15
  }'
```

---

### Inventory Management (Admin)

#### 12. Get Room Inventory

```bash
curl -X GET "http://localhost:8000/admin/inventory/rooms/1?start_date=2026-02-01&end_date=2026-02-28" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 13. Update Inventory

```bash
curl -X PATCH "http://localhost:8000/admin/inventory/rooms/1?start_date=2026-02-14&end_date=2026-02-16" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "surge_factor": 1.5,
    "price": 449.99
  }'
```

---

### Hotel Browse (Public)

#### 14. Search Hotels

```bash
curl -X GET "http://localhost:8000/hotels/search?city=New%20York&check_in_date=2026-03-01&check_out_date=2026-03-05&rooms_count=1"
```

**Response:**

```json
[
  {
    "id": 1,
    "name": "Grand Hyatt NYC",
    "city": "New York",
    "min_price": 299.99,
    "photos": ["https://example.com/photo1.jpg"],
    "amenities": ["wifi", "pool", "gym"]
  }
]
```

#### 15. Get Hotel Info

```bash
curl -X GET http://localhost:8000/hotels/1/info
```

---

### Booking Flow

#### 16. Initialize Booking

```bash
curl -X POST http://localhost:8000/bookings/init \
  -H "Authorization: Bearer YOUR_TOKEN" \
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

#### 17. Add Guests to Booking

```bash
curl -X POST http://localhost:8000/bookings/1/addGuests \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[1, 2]'
```

#### 18. Initiate Payment

```bash
curl -X POST http://localhost:8000/bookings/1/payments \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**

```json
{
  "session_url": "https://checkout.stripe.com/pay/cs_test_..."
}
```

#### 19. Check Booking Status

```bash
curl -X GET http://localhost:8000/bookings/1/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 20. Cancel Booking

```bash
curl -X POST http://localhost:8000/bookings/1/cancel \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### User Profile

#### 21. Get Profile

```bash
curl -X GET http://localhost:8000/users/profile \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 22. Update Profile

```bash
curl -X PATCH http://localhost:8000/users/profile \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "date_of_birth": "1990-01-15",
    "gender": "MALE"
  }'
```

#### 23. Get My Bookings

```bash
curl -X GET http://localhost:8000/users/myBookings \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### Guest Management

#### 24. Create Guest

```bash
curl -X POST http://localhost:8000/users/guests \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "gender": "FEMALE",
    "age": 28
  }'
```

#### 25. Get All Guests

```bash
curl -X GET http://localhost:8000/users/guests \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 26. Update Guest

```bash
curl -X PUT http://localhost:8000/users/guests/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "age": 29
  }'
```

#### 27. Delete Guest

```bash
curl -X DELETE http://localhost:8000/users/guests/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### Hotel Reports (Admin)

#### 28. Get Hotel Bookings

```bash
curl -X GET http://localhost:8000/admin/hotels/1/bookings \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 29. Get Hotel Report

```bash
curl -X GET "http://localhost:8000/admin/hotels/1/reports?start_date=2026-01-01&end_date=2026-12-31" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**

```json
{
  "hotel_id": 1,
  "total_bookings": 42,
  "total_revenue": 52499.58,
  "start_date": "2026-01-01",
  "end_date": "2026-12-31"
}
```

---

## 🧪 Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v

# Run specific test
pytest tests/test_auth.py::test_signup -v
```

---

## 📁 Project Structure

```
app/
├── main.py              # FastAPI application entry
├── config.py            # Environment configuration
├── database.py          # SQLAlchemy async setup
├── models/              # 7 SQLAlchemy ORM models
├── schemas/             # Pydantic request/response DTOs
├── routers/             # 8 API router modules
├── services/            # Business logic layer
├── security/            # JWT & authentication
└── exceptions/          # Global error handlers
tests/
├── conftest.py          # Pytest fixtures
├── test_auth.py         # Auth endpoint tests
├── test_hotels.py       # Hotel management tests
├── test_rooms.py        # Room management tests
├── test_bookings.py     # Booking flow tests
└── test_users.py        # User profile tests
```

---

## 🔧 Environment Variables

| Variable                      | Description                  | Default               |
| ----------------------------- | ---------------------------- | --------------------- |
| `DATABASE_URL`                | PostgreSQL connection string | Required              |
| `SECRET_KEY`                  | JWT signing key              | Required              |
| `ALGORITHM`                   | JWT algorithm                | HS256                 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token TTL             | 30                    |
| `REFRESH_TOKEN_EXPIRE_DAYS`   | Refresh token TTL            | 7                     |
| `STRIPE_API_KEY`              | Stripe secret key            | Required              |
| `STRIPE_WEBHOOK_SECRET`       | Stripe webhook secret        | Required              |
| `FRONTEND_URL`                | Frontend URL for redirects   | http://localhost:3000 |

---

## 📄 License

MIT
