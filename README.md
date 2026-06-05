# saas-billing-api

A multi-tenant SaaS billing system built with FastAPI.

## Tech Stack
- **API**: FastAPI + Pydantic
- **Database**: PostgreSQL + SQLAlchemy + Alembic
- **Auth**: JWT + role-based permissions
- **Background Jobs**: Celery + Redis
- **Infra**: Docker + Docker Compose
- **Testing**: pytest

## How to Run
```bash
uvicorn backend.app.main:app --reload
```
- Health check: http://localhost:8000/health
- API docs: http://localhost:8000/docs

## Build Roadmap

### Phase 1 — Project Skeleton
- Folder structure, requirements, virtual environment
- Basic FastAPI app with `/health` endpoint
- Docker + Docker Compose

### Phase 2 — Core Data Models
- SQLAlchemy models: Tenant, User, SubscriptionPlan, Subscription
- Alembic migrations + database session setup

### Phase 3 — Auth
- JWT authentication (login, token generation, verification)
- Role-based permissions (admin vs. user)

### Phase 4 — Billing Logic
- Invoice and LineItem models
- Invoice generation routes and CRUD

### Phase 5 — Background Jobs
- Celery + Redis setup
- Scheduled invoice generation task

### Phase 6 — Testing
- pytest suite for routes and services
