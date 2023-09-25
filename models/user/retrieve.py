import schemas.user

from models.user.user import User
from sqlalchemy import Select, select, and_
from sqlalchemy.orm import Session
from uuid import UUID


def read_users(session: Session, name_like: str, surname_like: str, 
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
    
    query_result = session.execute(sql_statement).all()
    for record in query_result:
        users.append(schemas.user.User(**{k: v for k, v in record[0].__dict__.items() 
                      if not k.startswith('_')}))    
    
    return users


def read_user_by_id(session: Session, user_id: UUID, include_deleted: bool) -> schemas.user.User | None:

    user: schemas.user.User = None
    
    sql_statement: Select = select(User) \
                            .where(and_( \
                                True if include_deleted else User.deleted_at.is_(None),
                                User.id == user_id)) \
                            .order_by(User.created_at)             
    
    query_result = session.scalars(sql_statement).one_or_none()
    if query_result:
        user = schemas.user.User(**{k: v for k, v in query_result.__dict__.items() if not k.startswith('_')})

        return user

    return None