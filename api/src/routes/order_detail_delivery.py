from fastapi import APIRouter, HTTPException, status

from src.models.order_detail_delivery import (
    OrderDetailDelivery,
    OrderDetailDeliveryCreate,
    OrderDetailDeliveryUpdate,
)
from src.repositories.order_detail_deliveries_repo import get_order_detail_deliveries_repository
from src.utils.errors import DatabaseError, NotFoundError

router = APIRouter(prefix="/order-detail-deliveries",
                   tags=["order-detail-deliveries"])


@router.get("", response_model=list[OrderDetailDelivery])
def get_all_order_detail_deliveries():
    repo = get_order_detail_deliveries_repository()
    return repo.find_all()


@router.get("/{order_detail_delivery_id}", response_model=OrderDetailDelivery)
def get_order_detail_delivery(order_detail_delivery_id: int):
    repo = get_order_detail_deliveries_repository()
    odd = repo.find_by_id(order_detail_delivery_id)

    if not odd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order detail delivery with id {order_detail_delivery_id} not found"
        )

    return odd


@router.post("", response_model=OrderDetailDelivery, status_code=status.HTTP_201_CREATED)
def create_order_detail_delivery(odd_data: OrderDetailDeliveryCreate):
    repo = get_order_detail_deliveries_repository()

    try:
        return repo.create(odd_data.model_dump(by_alias=False, exclude_unset=True))
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e


@router.put("/{order_detail_delivery_id}", response_model=OrderDetailDelivery)
def update_order_detail_delivery(order_detail_delivery_id: int, odd_data: OrderDetailDeliveryUpdate):
    repo = get_order_detail_deliveries_repository()

    try:
        return repo.update(order_detail_delivery_id, odd_data.model_dump(by_alias=False, exclude_unset=True))
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e


@router.delete("/{order_detail_delivery_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_detail_delivery(order_detail_delivery_id: int):
    repo = get_order_detail_deliveries_repository()

    try:
        repo.delete(order_detail_delivery_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e
