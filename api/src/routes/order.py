from fastapi import APIRouter, HTTPException, status

from src.models.order import Order, OrderCreate, OrderUpdate
from src.repositories.orders_repo import get_orders_repository
from src.utils.errors import DatabaseError, NotFoundError

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=list[Order])
def get_all_orders():
    repo = get_orders_repository()
    return repo.find_all()


@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int):
    repo = get_orders_repository()
    order = repo.find_by_id(order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )

    return order


@router.post("", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreate):
    repo = get_orders_repository()

    try:
        return repo.create(order_data.model_dump(by_alias=False, exclude_unset=True))
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e


@router.put("/{order_id}", response_model=Order)
def update_order(order_id: int, order_data: OrderUpdate):
    repo = get_orders_repository()

    try:
        return repo.update(order_id, order_data.model_dump(by_alias=False, exclude_unset=True))
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int):
    repo = get_orders_repository()

    try:
        repo.delete(order_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e
