from fastapi import APIRouter, HTTPException, status

from src.models.branch import Branch, BranchCreate, BranchUpdate
from src.repositories.branches_repo import get_branches_repository
from src.utils.errors import DatabaseError, NotFoundError

router = APIRouter(prefix="/branches", tags=["branches"])


@router.get("", response_model=list[Branch])
def get_all_branches():
    repo = get_branches_repository()
    return repo.find_all()


@router.get("/{branch_id}", response_model=Branch)
def get_branch(branch_id: int):
    repo = get_branches_repository()
    branch = repo.find_by_id(branch_id)

    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Branch with id {branch_id} not found"
        )

    return branch


@router.post("", response_model=Branch, status_code=status.HTTP_201_CREATED)
def create_branch(branch_data: BranchCreate):
    repo = get_branches_repository()

    try:
        return repo.create(branch_data.model_dump(by_alias=False, exclude_unset=True))
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e


@router.put("/{branch_id}", response_model=Branch)
def update_branch(branch_id: int, branch_data: BranchUpdate):
    repo = get_branches_repository()

    try:
        return repo.update(branch_id, branch_data.model_dump(by_alias=False, exclude_unset=True))
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e


@router.delete("/{branch_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_branch(branch_id: int):
    repo = get_branches_repository()

    try:
        repo.delete(branch_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except DatabaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e
