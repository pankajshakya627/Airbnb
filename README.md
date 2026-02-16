<div align="center">

# 🏨 AirBnb FastAPI Backend

**Production-ready Hotel Booking API built with FastAPI, async SQLAlchemy & PostgreSQL**

[![CI Pipeline](https://github.com/pankajshakya627/Airbnb/actions/workflows/ci.yml/badge.svg)](https://github.com/pankajshakya627/Airbnb/actions/workflows/ci.yml)
[![CD Pipeline](https://github.com/pankajshakya627/Airbnb/actions/workflows/deploy.yml/badge.svg)](https://github.com/pankajshakya627/Airbnb/actions/workflows/deploy.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg)](https://fastapi.tiangolo.com)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🏨 Project Overview

A robust, production-ready Hotel Management & Booking System backend built with **FastAPI**. This project is a complete conversion of a legacy Spring Boot application to a modern, high-performance Python architecture. It features secure authentication, role-based access control, comprehensive booking flows, Stripe payment integration, and a full CI/CD pipeline with GitHub Actions & Docker.

## ✨ Key Features

- **Authentication & Security**: JWT-based auth, BCrypt password hashing, and Role-Based Access Control (RBAC) for Guests and Hotel Managers.
- **Hotel Management**: Complete CRUD for Hotels, Rooms, and Amenities.
- **Dynamic Inventory**: Intelligent room inventory management with surge pricing capabilities.
- **Booking Engine**: Full booking lifecycle management (Reservation -> Payment -> Confirmation -> Cancellation).
- **Payment Integration**: Seamless Stripe checkout integration with webhook handling.
- **Search & Filtering**: Optimized search functionality for finding available hotels by city and dates.
- **Database Migrations**: Automated schema management using Alembic.
- **Dockerized**: Fully containerized setup with health checks and multi-stage builds.
- **CI/CD Pipeline**: Automated linting, testing, Docker build & push via GitHub Actions.
- **Code Quality**: Enforced with Ruff linter/formatter and 77% test coverage.

## 🛠️ Tech Stack

| Category             | Technology                            |
| -------------------- | ------------------------------------- |
| **Framework**        | FastAPI (Python 3.12)                 |
| **Database**         | PostgreSQL 16                         |
| **ORM**              | SQLAlchemy 2.0 (Async + asyncpg)      |
| **Migrations**       | Alembic                               |
| **Validation**       | Pydantic v2                           |
| **Testing**          | Pytest + HTTPX (77% coverage)         |
| **Payments**         | Stripe API                            |
| **CI/CD**            | GitHub Actions                        |
| **Containerization** | Docker (multi-stage) + Docker Compose |
| **Code Quality**     | Ruff (linter + formatter)             |
| **Registry**         | GitHub Container Registry (GHCR)      |

---

## 🏗️ System Architecture

<p align="center">
  <img src="docs/diagrams/architecture.svg" alt="System Architecture" width="100%">
</p>

---

## 🔄 Booking Flow

<p align="center">
  <img src="docs/diagrams/booking-flow.svg" alt="Booking Lifecycle" width="100%">
</p>

---

## 🗄️ Database Schema

```mermaid
erDiagram
    USERS ||--o{ BOOKINGS : creates
    USERS ||--o{ HOTELS : owns
    USERS ||--o{ GUESTS : manages
    HOTELS ||--o{ ROOMS : contains
    HOTELS ||--o{ INVENTORY : tracks
    ROOMS ||--o{ INVENTORY : has
    ROOMS ||--o{ BOOKINGS : reserved_in
    BOOKINGS }o--o{ GUESTS : includes

    USERS {
        int id PK
        string email UK
        string password
        string name
        enum gender
        date date_of_birth
        array roles
    }

    HOTELS {
        int id PK
        string name
        string city
        array photos
        array amenities
        json contact_info
        bool active
        int owner_id FK
    }

    ROOMS {
        int id PK
        string type
        decimal base_price
        array photos
        array amenities
        int total_count
        int capacity
        int hotel_id FK
    }

    INVENTORY {
        int id PK
        date date
        int book_count
        int reserved_count
        int total_count
        decimal surge_factor
        decimal price
        bool closed
        int hotel_id FK
        int room_id FK
    }

    BOOKINGS {
        int id PK
        int rooms_count
        date check_in_date
        date check_out_date
        enum booking_status
        decimal amount
        int hotel_id FK
        int room_id FK
        int user_id FK
    }

    GUESTS {
        int id PK
        string name
        enum gender
        int age
        int user_id FK
    }
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 16+
- Docker (optional)

### Option 1: Docker (Recommended)

```bash
# Clone
git clone https://github.com/pankajshakya627/Airbnb.git
cd Airbnb

# Start everything
docker compose up -d

# Run migrations
docker compose exec app alembic upgrade head
```

### Option 2: Local Setup

```bash
# Create virtual environment
python3.12 -m venv venv
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

### Option 3: Pull from GHCR

```bash
# Login to GitHub Container Registry
echo "YOUR_GITHUB_PAT" | docker login ghcr.io -u YOUR_USERNAME --password-stdin

# Pull the latest image
docker pull ghcr.io/pankajshakya627/airbnb:latest

# Run with your database
docker run -d -p 8000:8000 \
  -e DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/airbnb \
  -e SECRET_KEY=your-secret-key \
  ghcr.io/pankajshakya627/airbnb:latest
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
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=term-missing --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v

# Run specific test class
pytest tests/test_bookings.py::TestInitializeBooking -v
```

**Current Coverage: 77%** across 56 tests covering auth, hotels, rooms, bookings, inventory, browse, and user management.

---

## 🔄 CI/CD Pipeline

<p align="center">
  <img src="docs/diagrams/ci-cd-pipeline.svg" alt="CI/CD Pipeline" width="100%">
</p>

| Stage      | Tool                   | What it does                                      |
| ---------- | ---------------------- | ------------------------------------------------- |
| **Lint**   | Ruff                   | Checks code style, import sorting, common bugs    |
| **Test**   | Pytest + PostgreSQL 16 | Runs 56 tests with service container + coverage   |
| **Build**  | Docker Buildx          | Multi-stage build with layer caching              |
| **Push**   | GHCR                   | Pushes to `ghcr.io/pankajshakya627/airbnb:latest` |
| **Deploy** | Configurable           | SSH, AWS ECS, or Railway (placeholder)            |

---

## ✅ Code Quality

```bash
# Lint
ruff check .

# Format
ruff format .

# Lint + auto-fix
ruff check . --fix
```

Enforced rules: `pycodestyle`, `pyflakes`, `isort`, `pyupgrade`, `flake8-bugbear`, `flake8-simplify`

---

## 📁 Project Structure

```
AirBnbfastapi/
├── .github/
│   └── workflows/
│       ├── ci.yml                     # CI: Lint → Test → Docker Build & Push
│       └── deploy.yml                 # CD: Deploy placeholder (SSH/ECS/Railway)
├── alembic/
│   ├── env.py                         # Alembic environment config
│   ├── script.py.mako                 # Migration template
│   └── versions/
│       └── beb29e1df7e9_initial.py    # Initial migration
├── app/
│   ├── __init__.py
│   ├── main.py                        # FastAPI app entry + lifespan
│   ├── config.py                      # Pydantic settings (env vars)
│   ├── database.py                    # SQLAlchemy async engine + session
│   ├── exceptions/
│   │   ├── __init__.py
│   │   └── handlers.py                # Global HTTP exception handlers
│   ├── models/                        # 7 SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── booking.py                 # Booking + guest M2M
│   │   ├── enums.py                   # BookingStatus, Gender, Role
│   │   ├── guest.py                   # Guest profile
│   │   ├── hotel.py                   # Hotel + amenities + contact
│   │   ├── hotel_min_price.py         # Min price computed column
│   │   ├── inventory.py               # Date-level room inventory
│   │   ├── room.py                    # Room type + pricing
│   │   └── user.py                    # User + roles
│   ├── routers/                       # 8 API route modules
│   │   ├── __init__.py
│   │   ├── auth.py                    # /auth/signup, /auth/login, /auth/refresh
│   │   ├── bookings.py                # /bookings/* CRUD
│   │   ├── browse.py                  # /hotels/search, /hotels/{id}/info
│   │   ├── hotels.py                  # /admin/hotels/* CRUD
│   │   ├── inventory.py               # /admin/inventory/* management
│   │   ├── rooms.py                   # /admin/hotels/{id}/rooms/* CRUD
│   │   ├── users.py                   # /users/profile, /users/guests/*
│   │   └── webhooks.py                # /webhooks/stripe
│   ├── schemas/                       # Pydantic v2 DTOs
│   │   ├── __init__.py
│   │   ├── booking.py                 # BookingCreate, BookingResponse
│   │   ├── common.py                  # Shared schemas
│   │   ├── guest.py                   # GuestCreate, GuestResponse
│   │   ├── hotel.py                   # HotelCreate, HotelResponse
│   │   ├── inventory.py               # InventoryUpdate, InventoryResponse
│   │   ├── room.py                    # RoomCreate, RoomResponse
│   │   └── user.py                    # UserCreate, UserResponse, Token
│   ├── security/
│   │   ├── __init__.py
│   │   ├── dependencies.py            # get_current_user, role_required
│   │   ├── jwt.py                     # JWT create/decode tokens
│   │   └── password.py                # BCrypt hash/verify
│   ├── services/                      # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py            # Signup, login, token refresh
│   │   ├── booking_service.py         # Booking lifecycle management
│   │   ├── checkout_service.py        # Stripe checkout integration
│   │   ├── guest_service.py           # Guest CRUD operations
│   │   ├── hotel_service.py           # Hotel CRUD + activation
│   │   ├── inventory_service.py       # Inventory queries + updates
│   │   ├── room_service.py            # Room CRUD + inventory init
│   │   └── user_service.py            # Profile management
│   └── utils/
│       └── __init__.py
├── docs/
│   ├── diagrams/                      # Animated SVG diagrams
│   │   ├── architecture.svg           # System architecture
│   │   ├── booking-flow.svg           # Booking lifecycle
│   │   └── ci-cd-pipeline.svg         # CI/CD pipeline
│   ├── GUIDE.md                       # Developer guide
│   ├── HLD.md                         # High-Level Design document
│   └── LLD.md                         # Low-Level Design document
├── tests/                             # 56 async tests (77% coverage)
│   ├── __init__.py
│   ├── conftest.py                    # Shared fixtures + async DB setup
│   ├── test_auth.py                   # Authentication tests
│   ├── test_bookings.py               # Booking flow tests
│   ├── test_browse.py                 # Hotel search tests
│   ├── test_hotels.py                 # Hotel management tests
│   ├── test_inventory.py              # Inventory management tests
│   ├── test_rooms.py                  # Room management tests
│   └── test_users.py                  # User profile tests
├── .dockerignore                      # Docker build exclusions
├── .env.example                       # Environment template
├── .gitignore
├── alembic.ini                        # Alembic configuration
├── docker-compose.yml                 # Local dev stack (app + PostgreSQL)
├── Dockerfile                         # Multi-stage build + HEALTHCHECK
├── pytest.ini                         # Pytest configuration
├── README.md
├── requirements.txt                   # Python dependencies
└── ruff.toml                          # Ruff linter/formatter config
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

## 📚 Documentation

- **[High-Level Design (HLD)](docs/HLD.md)** — Architecture, database design, system flows, interview Q&A
- **[Low-Level Design (LLD)](docs/LLD.md)** — Class diagrams, schemas, service layer, security implementation
- **[Swagger UI](http://localhost:8000/docs)** — Interactive API documentation (when running)

---

## 📄 License

MIT
