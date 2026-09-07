# FastAPI CRUD API

A production-oriented backend built with **FastAPI**, designed as a skeletal foundation for building scalable and maintainable REST APIs.

This project goes beyond basic CRUD operations by implementing concepts commonly used in production backend applications, including authentication, authorization, database management, validation, password security, and structured API architecture.

## 🚀 Features

* RESTful CRUD APIs
* JWT-based authentication
* User authentication & authorization
* Secure password hashing
* Protected API endpoints
* User profile management
* Account deletion with scheduled deletion
* Partial user updates using `PATCH`
* Pydantic request/response validation
* SQLAlchemy ORM integration
* SQLite database
* Dependency Injection with FastAPI
* Database session management
* Transaction handling with rollback
* Centralized HTTP error handling
* Modular API structure using `APIRouter`
* Automatic API documentation with Swagger/OpenAPI

## 🏗️ Architecture

The project follows a modular backend structure where different responsibilities are separated into their respective layers.

```text
Client
  │
  ▼
FastAPI Router
  │
  ├── Request Validation → Pydantic
  │
  ├── Authentication → JWT
  │
  ├── Business Logic
  │
  └── Database Operations → SQLAlchemy
                              │
                              ▼
                           Database
```

## 🛠️ Tech Stack

* **Python**
* **FastAPI**
* **Pydantic**
* **SQLAlchemy**
* **SQLite**
* **JWT**
* **Passlib / bcrypt**
* **Uvicorn**

## 🔐 Authentication Flow

Authentication is implemented using JWT bearer tokens.

```text
Login
  ↓
Verify credentials
  ↓
Generate JWT
  ↓
Return access token
  ↓
Client sends:
Authorization: Bearer <token>
  ↓
JWT validation
  ↓
Identify current user
  ↓
Access protected endpoint
```

## 📌 API Capabilities

### Authentication

* User registration
* User login
* JWT access tokens
* Current-user authentication
* Protected routes

### User Management

* Create users
* Retrieve users
* Update user information
* Change password
* Change email
* Delete/deactivate account
* Scheduled account deletion

### Database

SQLAlchemy is used as the ORM layer for interacting with the database.

The project also demonstrates:

* Session management
* Dependency-based database injection
* ORM models
* Transactions
* Commit & rollback
* Database constraints
* Query filtering

## 📖 What This Project Demonstrates

This project was built to understand how the individual components of a backend system work together rather than simply implementing isolated CRUD endpoints.

Key concepts explored include:

* FastAPI dependency injection
* Pydantic models vs SQLAlchemy models
* JWT authentication
* Password hashing
* ORM-based database interaction
* HTTP status codes
* Request/response validation
* Partial updates
* Database transactions
* Modular API design
* Authentication vs authorization

## ▶️ Running Locally

Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn main:app --reload
```

The interactive API documentation will then be available through FastAPI's Swagger UI.

## 🎯 Purpose

This repository serves as a **backend foundation and learning project** for understanding how production-oriented FastAPI applications are structured.

The architecture is intentionally kept extensible so that additional features such as role-based access control, PostgreSQL, Redis, background tasks, testing, Docker, and deployment can be incorporated as the project evolves.

## 🔮 Future Improvements

* PostgreSQL integration
* Alembic database migrations
* Role-based access control (RBAC)
* Automated testing with Pytest
* Dockerization
* Redis caching
* Background task processing
* Rate limiting
* CI/CD pipeline
* Production deployment
* Improved logging and monitoring

---

### Author

**Ayush Singh**

Built with Python, FastAPI, and a lot of debugging. 🚀
