from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.interface import (
    InterfaceCreate,
    InterfaceListResponse,
    InterfaceResponse,
    InterfaceStatusUpdate,
    InterfaceUpdate,
)
from app.services import interface_service

router = APIRouter()


def _get_or_404(db: Session, interface_id: int):
    interface = interface_service.get_interface(db, interface_id)
    if not interface:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interface not found")
    return interface


@router.get("", response_model=InterfaceListResponse)
def list_interfaces(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: str | None = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    total, items = interface_service.get_interfaces(db, page, page_size, keyword)
    return InterfaceListResponse(total=total, page=page, page_size=page_size, items=items)


@router.post("", response_model=InterfaceResponse, status_code=status.HTTP_201_CREATED)
def create_interface(
    data: InterfaceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return interface_service.create_interface(db, data, created_by=current_user.id)


@router.get("/{interface_id}", response_model=InterfaceResponse)
def get_interface(
    interface_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return _get_or_404(db, interface_id)


@router.put("/{interface_id}", response_model=InterfaceResponse)
def update_interface(
    interface_id: int,
    data: InterfaceUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    interface = _get_or_404(db, interface_id)
    return interface_service.update_interface(db, interface, data)


@router.delete("/{interface_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interface(
    interface_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    interface = _get_or_404(db, interface_id)
    interface_service.delete_interface(db, interface)


@router.patch("/{interface_id}/status", response_model=InterfaceResponse)
def update_status(
    interface_id: int,
    data: InterfaceStatusUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    interface = _get_or_404(db, interface_id)
    return interface_service.update_status(db, interface, data.is_enabled)
