from datetime import datetime
from typing import Any
from pydantic import BaseModel


class InterfaceCreate(BaseModel):
    name: str
    description: str | None = None
    method: str
    url: str
    headers: dict[str, Any] | None = None
    params: dict[str, Any] | None = None
    body: dict[str, Any] | None = None
    auth_type: str = "none"
    auth_config: dict[str, Any] | None = None
    category: str | None = None
    is_enabled: int = 1


class InterfaceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    method: str | None = None
    url: str | None = None
    headers: dict[str, Any] | None = None
    params: dict[str, Any] | None = None
    body: dict[str, Any] | None = None
    auth_type: str | None = None
    auth_config: dict[str, Any] | None = None
    category: str | None = None


class InterfaceStatusUpdate(BaseModel):
    is_enabled: int


class InterfaceResponse(BaseModel):
    id: int
    name: str
    description: str | None
    method: str
    url: str
    headers: dict[str, Any] | None
    params: dict[str, Any] | None
    body: dict[str, Any] | None
    auth_type: str
    auth_config: dict[str, Any] | None
    category: str | None
    is_enabled: int
    created_by: int | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class InterfaceListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[InterfaceResponse]
