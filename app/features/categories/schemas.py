from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


# --- BASE SCHEMA ---
class CategoryBase(BaseModel):
    name: str = Field(
        min_length=1, max_length=255, pattern=r"^[a-zA-Zа-яА-ЯёЁ0-9\s\-_]+$"
    )
    notation: Optional[str] = Field(None, min_length=1, max_length=500)
    current_budget_limit: Decimal = Field(
        default=Decimal("0.00"), ge=0, max_digits=20, decimal_places=2
    )


class CategoryRead(CategoryBase):
    id: int = Field(ge=1)
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None, 
        min_length=1, 
        max_length=255, 
        pattern=r"^[a-zA-Zа-яА-ЯёЁ0-9\s\-_]+$"
    )
    notation: Optional[str] = Field(
        default=None,
        min_length=1, 
        max_length=500, 
        pattern=r"^[a-zA-Zа-яА-ЯёЁ0-9\s\-_]+$"
    )
    current_budget_limit: Optional[Decimal] = Field(
        default=None, 
        ge=0, max_digits=20, decimal_places=2
    )


class CategoryFilters(BaseModel):
    ids: Optional[List[int]] = Field(default=None, min_length=1, max_length=1000)
    names: Optional[List[str]] = Field(default=None, min_length=1, max_length=1000)
    # notations: Optional[List[str]] = Field(default=None, min_length=1, max_length=1000)
    current_budget_limit: Optional[Decimal] = Field(default=None, ge=0)
    current_budget_limit_min: Optional[Decimal] = Field(default=None, ge=0)
    current_budget_limit_max: Optional[Decimal] = Field(default=None, ge=0)
    created_at: Optional[datetime] = None   
    created_at_from: Optional[datetime] = None
    created_at_to: Optional[datetime] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=50, ge=1, le=1000)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.created_at_from and self.created_at_to:
            if self.created_at_from > self.created_at_to:
                raise ValueError("created_at_from must be <= created_at_to")
        return self
