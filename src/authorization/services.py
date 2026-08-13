from fastapi import HTTPException, status
from .security import decode_access_token, create_access_token, create_refresh_token, get_password_hash, verify_password
from src.user.repositories import UserRepository
class AuthorizationService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register_user(self, email: str):
