from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_token
from app.mocks.fake_db import fake_users_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token, "access")

        if payload["type"] != "access":
            raise Exception()
        
        user_id = payload.get("user_id")

        if not user_id:
            raise Exception()
        
        user = fake_users_db.get(user_id) # REAL DB TODO!!!
        
        if not user or user["disabled"] or not user["is_verified"]:
            raise Exception()
        
        return user
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )