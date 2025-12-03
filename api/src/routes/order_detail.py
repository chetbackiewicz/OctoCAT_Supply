from fastapi import APIRouter, HTTPException, status

from src.models.order_detail import OrderDetail, OrderDetailCreate, OrderDetailUpdate
from src.repositories.order_details_repo import get_order_details_repository
from src.utils.errors import DatabaseError, NotFoundError

router = APIRouter(prefix="/order-details", tags=["order-details"])


@router.get("", response_model=list[OrderDetail])
def get_all_order_details():
    repo = get_order_details_repository()
    return repo.find_all()


@router.get("/{order_detail_id}", response_model=OrderDetail)
def get_order_detail(order_detail_id: int):
    repo = get_order_details_repository()
    detail = repo.find_by_id(order_detail_id)

    if not detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order detail with id {order_detail_id} not found"
        )

    return detail


@router.post("", response_model=OrderDetail, status_code=status.HTTP_201_CREATED)
def create_order_detail(detail_data: OrderDetailCreate):
    repo = get_order_details_repository()

    try:
        return repo.create(detail_data.model_dump(by_alias=False, exclude_unset=True))
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e


@router.put("/{order_detail_id}", response_model=OrderDetail)
def update_order_detail(order_detail_id: int, detail_data: OrderDetailUpdate):
    repo = get_order_details_repository()

    try:
        return repo.update(order_detail_id, detail_data.model_dump(by_alias=False, exclude_unset=True))
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e


@router.delete("/{order_detail_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_detail(order_detail_id: int):
    repo = get_order_details_repository()

    try:
        repo.delete(order_detail_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e
