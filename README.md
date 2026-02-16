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

```mermaid
flowchart TB
    subgraph Client["🌐 Client Layer"]
        WEB["Web App"]
        MOB["Mobile App"]
        API_DOC["Swagger /docs"]
    end

    subgraph Gateway["🔐 API Gateway"]
        FP["FastAPI\n+ CORS Middleware"]
        JWT["JWT Auth\n+ RBAC"]
    end

    subgraph Routers["📡 Router Layer"]
        direction LR
        R1["Auth"]
        R2["Hotels"]
        R3["Rooms"]
        R4["Bookings"]
        R5["Inventory"]
        R6["Browse"]
        R7["Users"]
        R8["Webhooks"]
    end

    subgraph Services["⚙️ Service Layer"]
        direction LR
        S1["AuthService"]
        S2["HotelService"]
        S3["BookingService"]
        S4["InventoryService"]
        S5["CheckoutService"]
    end

    subgraph Data["💾 Data Layer"]
        ORM["SQLAlchemy\nAsync ORM"]
        PG[("PostgreSQL 16")]
    end

    subgraph External["🌍 External"]
        STRIPE["Stripe API"]
    end

    Client --> Gateway
    FP --> JWT
    JWT --> Routers
    Routers --> Services
    Services --> ORM
    ORM --> PG
    S5 --> STRIPE

    style Client fill:#1a1a2e,stroke:#e94560,color:#eee
    style Gateway fill:#16213e,stroke:#0f3460,color:#eee
    style Routers fill:#0f3460,stroke:#533483,color:#eee
    style Services fill:#533483,stroke:#e94560,color:#eee
    style Data fill:#1a1a2e,stroke:#e94560,color:#eee
    style External fill:#16213e,stroke:#0f3460,color:#eee
```

---

## 🔄 Booking Flow

```mermaid
sequenceDiagram
    actor Guest
    participant API as FastAPI
    participant BS as BookingService
    participant INV as Inventory
    participant DB as PostgreSQL
    participant PAY as Stripe

    rect rgb(30, 40, 60)
        Note over Guest,DB: 1️⃣ Search & Reserve
        Guest->>API: POST /bookings/init
        API->>BS: initialise_booking()
        BS->>DB: Check availability
        DB-->>BS: Available ✅
        BS->>INV: Reserve rooms
        INV->>DB: UPDATE reserved_count
        BS->>DB: INSERT booking (RESERVED)
        DB-->>API: Booking created
        API-->>Guest: {status: RESERVED, amount: $599}
    end

    rect rgb(40, 50, 70)
        Note over Guest,PAY: 2️⃣ Add Guests & Pay
        Guest->>API: POST /bookings/{id}/addGuests
        API->>DB: Link guests → booking
        API-->>Guest: {status: GUESTS_ADDED}
        Guest->>API: POST /bookings/{id}/payments
        API->>PAY: Create checkout session
        PAY-->>API: session_url
        API-->>Guest: {session_url: "https://stripe.com/..."}
    end

    rect rgb(30, 60, 40)
        Note over PAY,DB: 3️⃣ Payment Confirmation
        PAY->>API: POST /webhook (payment.success)
        API->>BS: confirm_booking()
        BS->>INV: Move reserved → booked
        BS->>DB: UPDATE status = CONFIRMED
    end
```

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

```mermaid
flowchart LR
    subgraph CI["🔁 CI Pipeline"]
        direction LR
        PUSH["📤 Push to main"] --> LINT["🔍 Lint\n(Ruff)"]
        LINT --> TEST["🧪 Test\n(56 tests + PostgreSQL)"]
        TEST --> BUILD["🐳 Build\nDocker Image"]
        BUILD --> PUSH_IMG["📦 Push to\nGHCR"]
    end

    subgraph CD["🚀 CD Pipeline"]
        direction LR
        PULL["📥 Pull\nLatest Image"] --> DEPLOY["🚀 Deploy\n(SSH/ECS/Railway)"]
        DEPLOY --> HEALTH["❤️ Health\nCheck"]
    end

    CI --> CD

    style CI fill:#1a1a2e,stroke:#e94560,color:#eee
    style CD fill:#16213e,stroke:#0f3460,color:#eee
```

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
├── .github/workflows/     # CI/CD pipeline
│   ├── ci.yml             # Lint → Test → Docker Build
│   └── deploy.yml         # Deployment placeholder
├── app/
│   ├── main.py            # FastAPI application entry
│   ├── config.py          # Environment configuration
│   ├── database.py        # SQLAlchemy async setup
│   ├── models/            # 7 SQLAlchemy ORM models
│   ├── schemas/           # Pydantic v2 request/response DTOs
│   ├── routers/           # 8 API router modules
│   ├── services/          # Business logic layer
│   ├── security/          # JWT & RBAC authentication
│   └── exceptions/        # Global error handlers
├── tests/                 # 56 async tests (77% coverage)
├── docs/
│   ├── HLD.md             # High-Level Design document
│   └── LLD.md             # Low-Level Design document
├── Dockerfile             # Multi-stage build + HEALTHCHECK
├── docker-compose.yml     # Local development stack
├── ruff.toml              # Linter/formatter configuration
└── .dockerignore          # Docker build exclusions
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
