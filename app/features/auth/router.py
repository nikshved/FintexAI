from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import RegisterRequest, TokenResponse
from .service import AuthService


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register")
async def register(data: RegisterRequest):

    await AuthService.register(data.username, data.email, data.password)

    return {
        "message": "User registered. Please check your email to verify your account."
    }


@auth_router.get("/verify-email", response_model=TokenResponse)
def verify_email(token: str, response: Response):
    tokens = AuthService.verify_email(token)

    if not tokens:
        raise HTTPException(400, "Invalid token")

    access, refresh = tokens

    response.set_cookie(
        key="refresh_token",
        value=refresh,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
    )

    return {"access_token": access, "token_type": "bearer"}


@auth_router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), response: Response = None):

    tokens = AuthService.login(form_data.username, form_data.password)

    if not tokens:
        raise HTTPException(401, "Invalid credentials")

    access, refresh = tokens

    response.set_cookie(
        key="refresh_token",
        value=refresh,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
    )

    return {"access_token": access, "token_type": "bearer"}


@auth_router.post("/refresh", response_model=TokenResponse)
def refresh(request: Request, response: Response):

    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(401, "Missing refresh token")

    tokens = AuthService.refresh(refresh_token)

    if not tokens:
        raise HTTPException(401, "Invalid refresh token")

    access, new_refresh = tokens

    response.set_cookie(
        key="refresh_token",
        value=new_refresh,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
    )

    return {"access_token": access, "token_type": "bearer"}


@auth_router.post("/logout")
def logout(request: Request, response: Response):

    refresh_token = request.cookies.get("refresh_token")

    if refresh_token:
        AuthService.logout(refresh_token)

    response.delete_cookie("refresh_token")

    return {"message": "Logged out"}
