import os
from unittest.mock import Mock

import pytest
from httpx import ASGITransport, AsyncClient

# Set environment variable to use in-memory database for tests
os.environ["DATABASE_PATH"] = ":memory:"


@pytest.fixture
async def client():
    """Create test client with in-memory database."""
    from src.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_products_repo():
    """Create a mock products repository."""
    return Mock()


@pytest.fixture
def mock_suppliers_repo():
    """Create a mock suppliers repository."""
    return Mock()
