from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import status

from core.config import ALLOWED_TYPES
from core.config import MAX_FILE_SIZE
from src.common.storage import StorageFile

from .repositories import HouseRepositories
from src.user.repositories import UserRepository
from src.common.models import UserTypes


class HouseService:

    def __init__(self, repo: HouseRepositories, user_repo: UserRepository, storage: StorageFile):
        self.repo = repo
        self.user_repo = user_repo
        self.storage = storage

    async def get_house(self, house_id):
        house = self.repo.get_house(house_id)
        if house:
            return house
        else:
            raise HTTPException(status_code=401, detail=f"House with id - {house_id} not found")\


    async def create_house(self, data: dict, manager_id: int):
        developer = await self.user_repo.get_user(manager_id)

        if not developer:
            raise HTTPException(status_code=401, detail='developer return None')
        if developer.user_type == UserTypes.Developer:
            data_with_manager = {**data, 'manager_id': manager_id}
            new_house = await self.repo.create_house(data=data_with_manager)
            return new_house
        else:
            raise HTTPException(status_code=401, detail='This user, is not developer')

    async def delete_house(self, house_id: int, manager_id: int):
        house = await self.repo.get_house(house_id)

        if not house:
            raise HTTPException(status_code=400, detail='The house is not found')
        if house.manager_id != manager_id:
            raise HTTPException(status_code=403, detail='You are not the need manager')
        await self.repo.delete_house(house)
        return None

    async def update_house(self, house_data: dict, manager_id: int):
        pass
