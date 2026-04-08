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


class InterfaceDebugResponse(BaseModel):
    success: bool
    status_code: int | None
    duration_ms: int
    data: Any | None
    error_message: str | None


class InterfaceDebugRequest(BaseModel):
    headers: dict[str, Any] | None = None
    params: dict[str, Any] | None = None
    body: dict[str, Any] | None = None


class InterfaceTestCaseCreate(BaseModel):
    name: str
    description: str | None = None
    request_headers: dict[str, Any] | None = None
    request_params: dict[str, Any] | None = None
    request_body: dict[str, Any] | None = None
    expected_status: int | None = None
    expected_keywords: str | None = None
    remark: str | None = None


class InterfaceTestCaseResponse(BaseModel):
    id: int
    interface_id: int
    name: str
    description: str | None
    request_headers: dict[str, Any] | None
    request_params: dict[str, Any] | None
    request_body: dict[str, Any] | None
    expected_status: int | None
    expected_keywords: str | None
    remark: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
