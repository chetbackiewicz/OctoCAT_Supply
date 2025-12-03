from fastapi import APIRouter, HTTPException, status

from src.models.delivery import Delivery, DeliveryCreate, DeliveryUpdate
from src.repositories.deliveries_repo import get_deliveries_repository
from src.utils.errors import DatabaseError, NotFoundError

router = APIRouter(prefix="/deliveries", tags=["deliveries"])


@router.get("", response_model=list[Delivery])
def get_all_deliveries():
    repo = get_deliveries_repository()
    return repo.find_all()


@router.get("/{delivery_id}", response_model=Delivery)
def get_delivery(delivery_id: int):
    repo = get_deliveries_repository()
    delivery = repo.find_by_id(delivery_id)

    if not delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Delivery with id {delivery_id} not found"
        )

    return delivery


@router.post("", response_model=Delivery, status_code=status.HTTP_201_CREATED)
def create_delivery(delivery_data: DeliveryCreate):
    repo = get_deliveries_repository()

    try:
        return repo.create(delivery_data.model_dump(by_alias=False, exclude_unset=True))
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e


@router.put("/{delivery_id}", response_model=Delivery)
def update_delivery(delivery_id: int, delivery_data: DeliveryUpdate):
    repo = get_deliveries_repository()

    try:
        return repo.update(delivery_id, delivery_data.model_dump(by_alias=False, exclude_unset=True))
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e


@router.delete("/{delivery_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_delivery(delivery_id: int):
    repo = get_deliveries_repository()

    try:
        repo.delete(delivery_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e
