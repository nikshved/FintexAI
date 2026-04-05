from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from app.features.auth.router import auth_router
from app.features.auth.dependencies import get_current_user
from app.features.wallets.router import wallets_router
from seeds.products_seed import fake_products_db


app = FastAPI(
    title="Store API",
    description="API for store",
    version="1.0.0"
)


# --- Разрешаем запросы с любого фронтенда (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   

@app.get("/")    
async def root():
    return {"message": "Store API"}

@app.get("/me")
async def me(current_user = Depends(get_current_user)):
    return {
        "username": current_user["username"],
        "email": current_user["email"],
        "is_verified": current_user["is_verified"]
    }

app.include_router(auth_router)
app.include_router(wallets_router)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
