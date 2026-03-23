from datetime import datetime, timezone

from app.core.hashing import hash_password, verify_password
from app.core.security import create_access_token, create_refresh_token, create_verify_token, decode_token
from app.mocks.fake_db import fake_users_db, fake_refresh_tokens
from app.core.mail import send_verification_email
from app.core.config import settings


class AuthService:

    @staticmethod
    async def register(username: str, email: str, password: str):
        if email in fake_users_db["1"]["email"] and fake_users_db["1"]["is_verified"]: # REAL DB TODO!!!
            raise Exception("User exists")
        
        fake_users_db["2"] = {
            "username": username,
            "full_name": "",
            "email": email,
            "hashed_password": hash_password(password),
            "is_verified": False,
            "disabled": False,
            "ceated_at": datetime.now(timezone.utc),    
        }
        
        verify_token = create_verify_token(username)

        verify_link = f"{settings.CLIENT_HOST_PROTOCOL}://{settings.CLIENT_HOST}:{settings.CLIENT_PORT}/auth/verify-email?token={verify_token}"

        await send_verification_email(email, verify_link)
        
        return verify_token

    @staticmethod
    def verify_email(token: str):
        payload = decode_token(token, "verify")
        
        if payload["type"] != "verify":
            return None
        
        username = payload["sub"]
        user = fake_users_db.get(username)
        
        if not user:
            return None

        user["is_verified"] = True

        access = create_access_token(username)
        refresh = create_refresh_token(username)
        fake_refresh_tokens[refresh] = username

        return access, refresh

    @staticmethod
    def login(username: str, password: str):
        user = fake_users_db.get(username)
        if not user:
            return None
        if not verify_password(password, user["hashed_password"]):
            return None
        if not user["is_verified"]:
            raise Exception("Email not verified")
        if user["disabled"]:
            raise Exception("User disabled")

        access = create_access_token(username)
        refresh = create_refresh_token(username)
        fake_refresh_tokens[refresh] = username

        return access, refresh

    @staticmethod
    def refresh(refresh_token: str):
        payload = decode_token(refresh_token, "refresh")
        if payload["type"] != "refresh":
            return None

        username = fake_refresh_tokens.get(refresh_token)
        if not username:
            return None

        return create_access_token(username)

    @staticmethod
    def logout(refresh_token: str):
        if refresh_token in fake_refresh_tokens:
            del fake_refresh_tokens[refresh_token]