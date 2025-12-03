from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.db.connection import get_db
from src.models.product import Product, ProductCreate, ProductUpdate
from src.repositories.products_repo import ProductsRepository, get_products_repository
from src.utils.errors import DatabaseError, NotFoundError

router = APIRouter(prefix="/products", tags=["products"])

# Dependency type alias for cleaner code
ProductsRepo = Annotated[ProductsRepository, Depends(get_products_repository)]


@router.get("", response_model=list[Product])
def get_all_products(repo: ProductsRepo) -> list[Product]:
    """Get all products."""
    products = repo.find_all()
    return products


@router.get("/search")
def search_products(
    q: str = Query(..., description="Search products by name")
):
    """
    Search products by name.

    WARNING: This endpoint is INTENTIONALLY VULNERABLE to SQL injection for demo purposes.
    DO NOT use in production!
    """
    # VULNERABLE: Direct string concatenation in SQL query - CodeQL should detect this
    with get_db() as conn:
        cursor = conn.cursor()
        # This is intentionally vulnerable - user input directly in query string
        query = f"SELECT * FROM products WHERE name LIKE '%{q}%'"
        cursor.execute(query)
        results = cursor.fetchall()

        # Convert sqlite3.Row to dict
        products = []
        for row in results:
            products.append(dict(row))

        return products


@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int, repo: ProductsRepo) -> Product:
    """Get a product by ID."""
    product = repo.find_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )

    return product


@router.post("", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate, repo: ProductsRepo) -> Product:
    """Create a new product."""
    try:
        created = repo.create(product_data.model_dump(
            by_alias=False, exclude_unset=True))
        return created
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e


@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int, product_data: ProductUpdate, repo: ProductsRepo
) -> Product:
    """Update a product by ID."""
    try:
        updated = repo.update(
            product_id, product_data.model_dump(
                by_alias=False, exclude_unset=True)
        )
        return updated
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, repo: ProductsRepo) -> None:
    """Delete a product by ID."""
    try:
        repo.delete(product_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e
