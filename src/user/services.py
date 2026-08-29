import magic
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import status

from core.config import ALLOWED_TYPES
from core.config import MAX_FILE_SIZE

from .repositories import UserRepository


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_user(self, user_id: int):
        user = await self.repo.get_user(user_id=user_id)

        if user:
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id - {user_id} not found",
            )

    async def update_user(self, user_data: dict, user_id: int):
        if (
            len(user_data.get("first_name", "").strip()) < 3
            or len(user_data.get("last_name", "").strip()) < 3
        ):
            raise HTTPException(400, detail="Херню написав, треба більше трьох букв")

        if len(user_data.get("tg_id").strip()) != 10:
            raise HTTPException(400, detail="Проблема з tg айдішніком")

        if await self.repo.get_user_by_email(user_data.get("email", "").strip()):
            raise HTTPException(400, detail="Хуйня твій email, такий існує")

        if await self.repo.get_user_by_tg_id(user_data.get("tg_id", "")):
            raise HTTPException(400, detail="Хуйня, твій айді в тг")

        updated_user = await self.update_user(user_data=user_data, user_id=user_id)
        return updated_user

    async def check_photo(self, file: UploadFile):
        head = await file.read(2048)
        await file.seek(0)
        mime = magic.Magic(mime=True)

        detected_type = mime.from_buffer(head)

        return detected_type

    async def update_profile_avatar(self, user_id: int, image: UploadFile, user: dict):
        if image.size > MAX_FILE_SIZE:
            raise HTTPException(400, detail="Дохуя важиш, давай щось поменше")

        if image.content_type not in ALLOWED_TYPES:
            raise HTTPException(400, detail="Та щось не той тип файлу")

        if self.check_photo(image) not in ALLOWED_TYPES:
            raise HTTPException(400, detail="ТИ чо мені скинув даун???")
