from fastapi import APIRouter, HTTPException, status

from src.models.headquarters import Headquarters, HeadquartersCreate, HeadquartersUpdate
from src.repositories.headquarters_repo import get_headquarters_repository
from src.utils.errors import DatabaseError, NotFoundError

router = APIRouter(prefix="/headquarters", tags=["headquarters"])


@router.get("", response_model=list[Headquarters])
def get_all_headquarters():
    repo = get_headquarters_repository()
    return repo.find_all()


@router.get("/{headquarters_id}", response_model=Headquarters)
def get_headquarters(headquarters_id: int):
    repo = get_headquarters_repository()
    hq = repo.find_by_id(headquarters_id)

    if not hq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Headquarters with id {headquarters_id} not found"
        )

    return hq


@router.post("", response_model=Headquarters, status_code=status.HTTP_201_CREATED)
def create_headquarters(hq_data: HeadquartersCreate):
    repo = get_headquarters_repository()

    try:
        return repo.create(hq_data.model_dump(by_alias=False, exclude_unset=True))
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e


@router.put("/{headquarters_id}", response_model=Headquarters)
def update_headquarters(headquarters_id: int, hq_data: HeadquartersUpdate):
    repo = get_headquarters_repository()

    try:
        return repo.update(headquarters_id, hq_data.model_dump(by_alias=False, exclude_unset=True))
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e


@router.delete("/{headquarters_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_headquarters(headquarters_id: int):
    repo = get_headquarters_repository()

    try:
        repo.delete(headquarters_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e
