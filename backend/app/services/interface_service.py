from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.interface import Interface
from app.schemas.interface import InterfaceCreate, InterfaceUpdate


def get_interfaces(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    keyword: str | None = None,
):
    query = db.query(Interface)
    if keyword:
        like = f"%{keyword}%"
        query = query.filter(
            or_(Interface.name.like(like), Interface.url.like(like), Interface.category.like(like))
        )
    total = query.count()
    items = query.order_by(Interface.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return total, items


def get_interface(db: Session, interface_id: int) -> Interface | None:
    return db.query(Interface).filter(Interface.id == interface_id).first()


def create_interface(db: Session, data: InterfaceCreate, created_by: int | None = None) -> Interface:
    interface = Interface(**data.model_dump(), created_by=created_by)
    db.add(interface)
    db.commit()
    db.refresh(interface)
    return interface


def update_interface(db: Session, interface: Interface, data: InterfaceUpdate) -> Interface:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(interface, field, value)
    db.commit()
    db.refresh(interface)
    return interface


def delete_interface(db: Session, interface: Interface) -> None:
    db.delete(interface)
    db.commit()


def update_status(db: Session, interface: Interface, is_enabled: int) -> Interface:
    interface.is_enabled = is_enabled
    db.commit()
    db.refresh(interface)
    return interface
