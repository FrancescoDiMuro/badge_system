import schemas.user
from models.utils import get_fields_from_model
from models.user.user import User
from sqlalchemy import Select, select, and_
from sqlalchemy.orm import Session
from uuid import UUID


def retrieve_users(session: Session, name_like: str, surname_like: str, 
                   email_like: str, include_deleted: bool) -> list[schemas.user.User]:
  
    users: list[schemas.user.User] = []
    
    sql_statement: Select = select(User) \
                            .where(
                                and_( \
                                    True if include_deleted else User.deleted_at.is_(None),
                                    User.name.like(name_like),
                                    User.surname.like(surname_like),
                                    User.email.like(email_like))
                                ) \
                            .order_by(User.created_at)
    
    query_result = session.scalars(sql_statement).all()

    users = [schemas.user.User(**get_fields_from_model(model)) for model in query_result]
    
    return users


def retrieve_user_by_id(session: Session, user_id: UUID, include_deleted: bool) -> schemas.user.User | None:
    
    sql_statement: Select = select(User) \
                            .where(
                                and_( \
                                    True if include_deleted else User.deleted_at.is_(None),
                                    User.id == user_id)
                                ) \
                            .order_by(User.created_at)
    
    query_result = session.scalars(sql_statement).one_or_none()
    if query_result:        
        user: schemas.user.User = schemas.user.User(**get_fields_from_model(query_result))

        return user

    return None