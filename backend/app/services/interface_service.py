from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.interface import Interface
from app.models.interface_log import InterfaceLog
from app.models.interface_test_case import InterfaceTestCase
from app.schemas.interface import InterfaceCreate, InterfaceTestCaseCreate, InterfaceUpdate
from app.utils.request_executor import execute_http_request

ERROR_MESSAGE_MAX_LENGTH = 512
RESPONSE_BODY_MAX_LENGTH = 60000


def _truncate_error_message(message: str | None) -> str | None:
    if not message:
        return None

    return message[:ERROR_MESSAGE_MAX_LENGTH]


def _truncate_response_body(body: str | None) -> str | None:
    if body is None:
        return None

    return body[:RESPONSE_BODY_MAX_LENGTH]


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


def debug_interface(
    db: Session,
    interface: Interface,
    triggered_by: int | None = None,
    headers: dict | None = None,
    params: dict | None = None,
    body: dict | None = None,
):
    request_headers = interface.headers if headers is None else headers
    request_params = interface.params if params is None else params
    request_body = interface.body if body is None else body

    result = execute_http_request(
        method=interface.method,
        url=interface.url,
        headers=request_headers,
        params=request_params,
        json_body=request_body,
        auth_type=interface.auth_type,
        auth_config=interface.auth_config,
    )

    log = InterfaceLog(
        interface_id=interface.id,
        request_method=interface.method,
        request_url=result.request_url,
        request_headers=result.request_headers,
        request_body=request_body,
        response_status=result.status_code,
        response_body=_truncate_response_body(result.response_body),
        response_time_ms=result.duration_ms,
        is_success=1 if result.success else 0,
        error_message=_truncate_error_message(result.error_message),
        triggered_by=triggered_by,
    )
    db.add(log)

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()

    return result


def create_test_case(db: Session, interface: Interface, data: InterfaceTestCaseCreate) -> InterfaceTestCase:
    test_case = InterfaceTestCase(
        interface_id=interface.id,
        **data.model_dump(),
    )
    db.add(test_case)
    db.commit()
    db.refresh(test_case)
    return test_case


def get_interface_test_cases(db: Session, interface_id: int) -> list[InterfaceTestCase]:
    return (
        db.query(InterfaceTestCase)
        .filter(InterfaceTestCase.interface_id == interface_id)
        .order_by(InterfaceTestCase.updated_at.desc(), InterfaceTestCase.id.desc())
        .all()
    )
