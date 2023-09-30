from io import BytesIO
from models.badge.badge import Badge
from qrcode.main import QRCode
from qrcode.image.pil import PilImage
from sqlalchemy import Select, select
from sqlalchemy.orm import Session
from uuid import UUID


def badge_is_deleted(session: Session, badge_id: UUID) -> bool:

    sql_statement: Select = select(Badge.deleted_at) \
                            .where(Badge.id == badge_id)
    
    return session.scalar(sql_statement) is not None


def badge_code_to_qr_code(badge_code: str) -> PilImage:

    qr_code = QRCode(version=3, box_size=10, border=1)
    
    qr_code.add_data(badge_code)
    
    qr_code_image: PilImage = qr_code.make_image()
    
    qr_code_image_buffer = BytesIO()
    qr_code_image.save(qr_code_image_buffer)
    qr_code_image_buffer.seek(0)

    return qr_code_image_buffer
