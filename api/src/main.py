import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.db.migrate import MigrationRunner
from src.db.seed import Seeder
from src.routes import (
    branch,
    delivery,
    headquarters,
    order,
    order_detail,
    order_detail_delivery,
    product,
    supplier,
)
from src.utils.errors import DatabaseError


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Run migrations and seed database
    migration_runner = MigrationRunner()
    applied_migrations = migration_runner.run_migrations()

    if applied_migrations:
        print(f"Applied migrations: {', '.join(applied_migrations)}")

    seeder = Seeder()
    seeded_tables = seeder.seed_database()

    if seeded_tables:
        print(f"Seeded tables: {', '.join(seeded_tables)}")

    yield
    # Shutdown: cleanup would go here if needed


app = FastAPI(
    title="OctoCAT Supply Chain Management API",
    description="Python/FastAPI implementation of the OctoCAT Supply Chain Management API",
    version="1.0.0",
    lifespan=lifespan,
)


def get_cors_origins() -> list[str]:
    cors_origins_env = os.getenv("CORS_ORIGINS", "")

    if cors_origins_env:
        base_origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]
    else:
        # Default origins for local development
        base_origins = [
            "http://localhost:5137",
            "http://localhost:3001",
            "http://127.0.0.1:5137",
            "http://127.0.0.1:3001",
        ]

    patterns = [
        r"https://.*\.preview\.app\.github\.dev",
        r"https://.*-\d+\.app\.github\.dev",
        r"https://.*\.azurecontainerapps\.io",
    ]

    return base_origins + patterns


# Separate exact origins from regex patterns
cors_config = get_cors_origins()
exact_origins = [o for o in cors_config if not o.startswith("http") or not any(c in o for c in ["*", ".+", ".*"])]
regex_patterns = [o for o in cors_config if o.startswith("http") and o not in exact_origins] + [o for o in cors_config if o.startswith("r\"") or (not o.startswith("http") and any(c in o for c in ["*", ".+", ".*"]))]

print(f"Configured CORS origins: {exact_origins}")
print(f"Configured CORS patterns: {regex_patterns}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=exact_origins if exact_origins else ["*"],
    allow_origin_regex="|".join(regex_patterns) if regex_patterns else None,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.exception_handler(DatabaseError)
async def database_exception_handler(request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal server error"},
    )


app.include_router(supplier.router, prefix="/api")
app.include_router(headquarters.router, prefix="/api")
app.include_router(branch.router, prefix="/api")
app.include_router(product.router, prefix="/api")
app.include_router(order.router, prefix="/api")
app.include_router(order_detail.router, prefix="/api")
app.include_router(delivery.router, prefix="/api")
app.include_router(order_detail_delivery.router, prefix="/api")


@app.get("/")
def read_root():
    return {
        "message": "OctoCAT Supply Chain Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
