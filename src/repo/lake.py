from src.core.base import BaseRepo
from src.db.model import Lake


class LakeRepo(BaseRepo[Lake]):
    def __init__(self) -> None:
        super().__init__(Lake)