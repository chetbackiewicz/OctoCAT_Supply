
from src.repositories.base_repo import BaseRepository


class HeadquartersRepository(BaseRepository):
    def __init__(self):
        super().__init__("headquarters", "headquarters_id")


def get_headquarters_repository() -> HeadquartersRepository:
    return HeadquartersRepository()
