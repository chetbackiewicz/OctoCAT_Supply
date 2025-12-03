from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.models.supplier import Supplier, SupplierCreate, SupplierUpdate
from src.repositories.suppliers_repo import SuppliersRepository, get_suppliers_repository
from src.utils.errors import DatabaseError, NotFoundError

router = APIRouter(prefix="/suppliers", tags=["suppliers"])

# Dependency type alias for cleaner code
SuppliersRepo = Annotated[SuppliersRepository,
                          Depends(get_suppliers_repository)]


@router.get("", response_model=list[Supplier])
def get_all_suppliers(repo: SuppliersRepo) -> list[Supplier]:
    """Get all suppliers."""
    suppliers = repo.find_all()
    return suppliers


@router.get("/{supplier_id}", response_model=Supplier)
def get_supplier(supplier_id: int, repo: SuppliersRepo) -> Supplier:
    """Get a supplier by ID."""
    supplier = repo.find_by_id(supplier_id)

    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier with id {supplier_id} not found"
        )

    return supplier


@router.post("", response_model=Supplier, status_code=status.HTTP_201_CREATED)
def create_supplier(supplier_data: SupplierCreate, repo: SuppliersRepo) -> Supplier:
    """Create a new supplier."""
    try:
        created = repo.create(supplier_data.model_dump(
            by_alias=False, exclude_unset=True))
        return created
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e


@router.put("/{supplier_id}", response_model=Supplier)
def update_supplier(
    supplier_id: int, supplier_data: SupplierUpdate, repo: SuppliersRepo
) -> Supplier:
    """Update a supplier by ID."""
    try:
        updated = repo.update(supplier_id, supplier_data.model_dump(
            by_alias=False, exclude_unset=True))
        return updated
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e


@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: int, repo: SuppliersRepo) -> None:
    """Delete a supplier by ID."""
    try:
        repo.delete(supplier_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e


def _log_supplier_action(action: str):
    """Log supplier action - procedure with no return value."""
    print(f"Supplier action: {action}")
    # Implicitly returns None


def _check_supplier_status(supplier: dict) -> str:
    """Check supplier status with mixed returns - triggers py/mixed-returns."""
    if supplier.get("active"):
        return "active"
    elif supplier.get("verified"):
        return "verified"
    # Implicit return (None) here - mixed with explicit returns


def _validate_supplier_with_lambda(suppliers: list[dict]):
    """Validate suppliers with unnecessary lambda - triggers py/unnecessary-lambda."""
    # Unnecessary lambda - just calls str()
    supplier_ids = map(lambda s: str(s.get("supplier_id")), suppliers)
    return list(supplier_ids)


def _process_supplier_action(action: str) -> bool:
    """Process action and use procedure return value incorrectly."""
    # Using return value of a procedure - triggers py/procedure-return-value-used
    result = _log_supplier_action(action)
    if result:  # This will always be None/False
        return True
    return False
