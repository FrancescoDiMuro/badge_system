import schemas.user

from models.utils import get_fields_from_model
from models.user.user import User
from sqlalchemy import Insert, insert
from sqlalchemy.orm import Session

def create_user(session: Session, user_post: dict) -> schemas.user.User:
    
    sql_statement: Insert = insert(User) \
                            .values(**user_post) \
                            .returning(User)
    
    query_result = session.scalars(sql_statement).one_or_none()
    if query_result:
        model_fields: dict = get_fields_from_model(query_result)
        user: schemas.user.User = schemas.user.User(**model_fields)
        session.commit()

        return user
