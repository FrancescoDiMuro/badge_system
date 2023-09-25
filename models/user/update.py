import schemas.user

from models.utils import get_fields_from_model
from models.user.user import User
from models.utils import now_with_timezone
from sqlalchemy import Update, update
from sqlalchemy.orm import Session
from uuid import UUID


def update_user(session: Session, user_id: UUID, user_update: dict) -> schemas.user.User:      

    user_update['updated_at'] = now_with_timezone()
        
    sql_statement: Update = update(User) \
                            .where(User.id == user_id) \
                            .values(**user_update) \
                            .returning(User)

    query_result: User = session.scalars(sql_statement).one_or_none()
    if query_result:
        model_fields: dict = get_fields_from_model(query_result)
        user: schemas.user.User = schemas.user.User(**model_fields)
        session.commit()

        return user
    