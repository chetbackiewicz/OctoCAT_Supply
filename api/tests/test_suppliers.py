
import pytest

from src.main import app
from src.repositories.suppliers_repo import get_suppliers_repository


@pytest.mark.asyncio
async def test_get_all_suppliers(client, mock_suppliers_repo):
    """Test getting all suppliers with mocked repository."""
    mock_suppliers = [
        {
            "supplier_id": i,
            "name": f"Supplier {i}",
            "contact_name": f"Contact {i}",
            "contact_email": f"contact{i}@example.com",
            "phone_number": f"555-000{i}",
            "address": f"{i} Test St",
            "city": "Test City",
            "state": "TS",
            "zip_code": f"{10000 + i}",
            "country": "Test Country",
        }
        for i in range(1, 11)
    ]
    mock_suppliers_repo.find_all.return_value = mock_suppliers

    app.dependency_overrides[get_suppliers_repository] = lambda: mock_suppliers_repo

    try:
        response = await client.get("/api/suppliers")
        assert response.status_code == 200

        suppliers = response.json()
        assert isinstance(suppliers, list)
        assert len(suppliers) == 10
        mock_suppliers_repo.find_all.assert_called_once()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_supplier_by_id(client, mock_suppliers_repo):
    """Test getting a supplier by ID with mocked repository."""
    mock_supplier = {
        "supplier_id": 1,
        "name": "OctoCat Supplies",
        "contact_name": "Mona Lisa",
        "contact_email": "mona@octocat.com",
        "phone_number": "555-0100",
        "address": "123 GitHub Way",
        "city": "San Francisco",
        "state": "CA",
        "zip_code": "94107",
        "country": "USA",
    }
    mock_suppliers_repo.find_by_id.return_value = mock_supplier

    app.dependency_overrides[get_suppliers_repository] = lambda: mock_suppliers_repo

    try:
        response = await client.get("/api/suppliers/1")
        assert response.status_code == 200

        supplier = response.json()
        assert supplier["supplierId"] == 1
        assert supplier["name"] == "OctoCat Supplies"
        mock_suppliers_repo.find_by_id.assert_called_once_with(1)
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_supplier(client, mock_suppliers_repo):
    """Test creating a supplier with mocked repository."""
    new_supplier = {
        "name": "New Supplier",
        "contactName": "Jane Doe",
        "contactEmail": "jane@new.com",
        "phoneNumber": "555-9999",
        "address": "456 New St",
        "city": "New City",
        "state": "NC",
        "zipCode": "12345",
        "country": "USA",
    }

    mock_created = {
        "supplier_id": 11,
        "name": "New Supplier",
        "contact_name": "Jane Doe",
        "contact_email": "jane@new.com",
        "phone_number": "555-9999",
        "address": "456 New St",
        "city": "New City",
        "state": "NC",
        "zip_code": "12345",
        "country": "USA",
    }
    mock_suppliers_repo.create.return_value = mock_created

    app.dependency_overrides[get_suppliers_repository] = lambda: mock_suppliers_repo

    try:
        response = await client.post("/api/suppliers", json=new_supplier)
        assert response.status_code == 201

        created = response.json()
        # The API returns camelCase field names via Pydantic aliases
        assert created["name"] == "New Supplier"
        assert "supplierId" in created
        mock_suppliers_repo.create.assert_called_once()
    finally:
        app.dependency_overrides.clear()
