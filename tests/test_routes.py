# app/routers/test_routes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated, Optional
from enum import Enum
from pydantic import BaseModel
import time


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

test_router = APIRouter(tags=["test"])

# Хранилище данных в памяти (для тестов)
test_db = {}

@test_router.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id_1": user_id}

@test_router.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@test_router.get("/items/")
async def read_item(skip: int = 0, limit: Optional[int]=None):
    if not limit:
        limit = 10
    return fake_items_db[skip : skip + limit]


@test_router.post("/items/")
async def read_item(item: Item):
    return {"item": item}

@test_router.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}

@test_router.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results