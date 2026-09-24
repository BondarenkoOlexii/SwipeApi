from fastapi import HTTPException
from fastapi import UploadFile

from src.common.models import ImageTypeChoice
from src.common.models import UserTypes
from src.common.storage import StorageFile
from src.user.repositories import UserRepository

from .repositories import HouseRepositories


class HouseService:
    def __init__(
        self, repo: HouseRepositories, user_repo: UserRepository, storage: StorageFile
    ):
        self.repo = repo
        self.user_repo = user_repo
        self.storage = storage

    async def _verify_house(self, house_id: int):
        house = await self.repo.get_house(house_id=house_id)
        if not house:
            raise HTTPException(status_code=404, detail="House doesnt found")
        return house

    def _verify_manager(self, manager_id: int, house):
        if house.manager_id != manager_id:
            raise HTTPException(status_code=403, detail="Your cant change this house")
        return house

    async def get_house(self, house_id):
        return await self._verify_house(house_id)

    async def create_house(self, data: dict, manager_id: int):
        developer = await self.user_repo.get_user(manager_id)

        if not developer:
            raise HTTPException(status_code=401, detail="developer return None")
        if developer.user_type == UserTypes.Developer:
            data_with_manager = {**data, "manager_id": manager_id}
            new_house = await self.repo.create_house(data=data_with_manager)
            return new_house
        else:
            raise HTTPException(status_code=401, detail="This user, is not developer")

    async def delete_house(self, house_id: int, manager_id: int):
        house = await self._verify_house(house_id)

        self._verify_manager(manager_id=manager_id, house=house)

        await self.repo.delete_house(house)
        return None

    async def update_house(self, house_data: dict, manager_id: int, house_id: int):
        house = await self._verify_house(house_id)

        self._verify_manager(manager_id=manager_id, house=house)

        new_house = await self.repo.update_house(house=house, data=house_data)

        return new_house

    async def upload_images(self, house_id: int, images: list[UploadFile]):
        images_list = []

        for image in images:
            check_image = self.storage.audit_photo(file=image)

            house_image = self.repo.get_house_images(house_id)

            if house_image:
                await self.storage.delete_file(check_image)

                new_image = await self.storage.download_file(image)

            else:
                new_image = await self.storage.download_file(image)

            uploaded_image = await self.repo.upload_file(
                house_id=house_id, file=new_image, type=ImageTypeChoice.Gallery
            )

            images_list.append(uploaded_image)

        return images_list
