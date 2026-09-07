import uuid
from pathlib import Path

import aiofiles
import aiofiles.os
from fastapi import UploadFile
from magic import magic

from core.config import CHUNK_SIZE
from core.config import UPLOAD_DIR


class StorageFile:
    def __init__(self, upload_dir: str | Path = UPLOAD_DIR):
        self.upload_dir = Path(upload_dir).resolve()

        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def check_photo(self, file: UploadFile):
        head = await file.read(2048)
        await file.seek(0)
        mime = magic.Magic(mime=True)

        detected_type = mime.from_buffer(head)

        return detected_type

    async def download_file(self, file: UploadFile):
        extension = Path(file.filename or "").suffix.lower()

        new_name = self.upload_dir / f"{uuid.uuid4()}{extension}"

        async with aiofiles.open(new_name, "wb") as buffer:
            while chunk := await file.read(CHUNK_SIZE):
                await buffer.write(chunk)
        return str(new_name)

    async def delete_file(self, name: str | None) -> bool:
        if not name:
            return False

        full_path = Path(name).resolve()

        if self.upload_dir not in full_path.parents:
            return False

        try:
            if full_path.is_file():
                await aiofiles.os.remove(full_path)
                return True

        except OSError:
            return False

        return False
