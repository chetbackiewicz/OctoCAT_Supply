
import pytest

from src.main import app
from src.repositories.products_repo import get_products_repository


@pytest.mark.asyncio
async def test_get_all_products(client, mock_products_repo):
    """Test getting all products with mocked repository."""
    mock_products = [
        {
            "product_id": i,
            "supplier_id": 1,
            "name": f"Product {i}",
            "description": f"Description {i}",
            "price": 100.0 + i,
            "sku": f"SKU-{i:03d}",
            "unit": "piece",
            "discount": 0.0,
        }
        for i in range(1, 13)
    ]
    mock_products_repo.find_all.return_value = mock_products

    # Override the dependency
    app.dependency_overrides[get_products_repository] = lambda: mock_products_repo

    try:
        response = await client.get("/api/products")
        assert response.status_code == 200

        products = response.json()
        assert isinstance(products, list)
        assert len(products) == 12
        mock_products_repo.find_all.assert_called_once()
    finally:
        # Clean up override
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_product_by_id(client, mock_products_repo):
    """Test getting a product by ID with mocked repository."""
    mock_product = {
        "product_id": 1,
        "supplier_id": 1,
        "name": "SmartFeeder One",
        "description": "Smart feeding system",
        "price": 129.99,
        "sku": "SF-001",
        "unit": "piece",
        "discount": 0.0,
    }
    mock_products_repo.find_by_id.return_value = mock_product

    app.dependency_overrides[get_products_repository] = lambda: mock_products_repo

    try:
        response = await client.get("/api/products/1")
        assert response.status_code == 200

        product = response.json()
        assert product["productId"] == 1
        assert product["name"] == "SmartFeeder One"
        assert product["price"] == 129.99
        mock_products_repo.find_by_id.assert_called_once_with(1)
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_product(client, mock_products_repo):
    """Test creating a product with mocked repository."""
    new_product = {
        "supplierId": 1,
        "name": "Test Product",
        "description": "A test product",
        "price": 99.99,
        "sku": "TEST-001",
        "unit": "piece",
        "discount": 0.1,
    }

    mock_created = {
        "product_id": 13,
        "supplier_id": 1,
        "name": "Test Product",
        "description": "A test product",
        "price": 99.99,
        "sku": "TEST-001",
        "unit": "piece",
        "discount": 0.1,
    }
    mock_products_repo.create.return_value = mock_created

    app.dependency_overrides[get_products_repository] = lambda: mock_products_repo

    try:
        response = await client.post("/api/products", json=new_product)
        assert response.status_code == 201

        created = response.json()
        assert created["name"] == "Test Product"
        assert created["price"] == 99.99
        assert "productId" in created
        mock_products_repo.create.assert_called_once()
    finally:
        app.dependency_overrides.clear()
