from sqlalchemy.orm import Session
from sqlalchemy import (Select, 
                        Insert, 
                        Update, 
                        select, 
                        insert, 
                        update, 
                        and_)

from sqlalchemy.exc import NoResultFound

from models.models import User
from uuid import UUID
from models.utils import now_with_timezone

def read_users(session: Session, name_like: str, surname_like: str, 
               email_like: str, include_deleted: bool) -> list[dict]:
  
    users: list = []
    
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
        users.append({k: v for k, v in record[0].__dict__.items() 
                      if not k.startswith('_')})    
    
    return users


def read_user_by_id(session: Session, user_id: UUID, include_deleted: bool) -> dict:

    user: dict = {}
    
    sql_statement: Select = select(User) \
                            .where(and_( \
                                True if include_deleted else User.deleted_at.is_(None),
                                User.id == user_id)) \
                            .order_by(User.created_at)             
    
    try:
        query_result = session.execute(sql_statement).one()[0]
    except NoResultFound:        
        return {}
    
    user = {k: v for k, v in query_result.__dict__.items() if not k.startswith('_')}

    return user


def create_user(session: Session, new_user: dict) -> dict:
    
    sql_statement: Insert = insert(User) \
                            .values(**new_user) \
                            .returning(User)
    
    user: dict = session.scalars(sql_statement).all()[0]
    user = {k: v for k, v in user.__dict__.items() if not k.startswith('_')}    

    if user:
        session.commit()

    return user


def user_is_deleted(session: Session, user_id: UUID) -> bool:

    sql_statement: Select = select(User.deleted_at) \
                            .where(User.id == user_id)
    
    return session.scalar(sql_statement) is not None


def update_user(session: Session, user_id: UUID, updated_user_info: dict):      

    user: dict = {}

    updated_user_info['updated_at'] = now_with_timezone()
        
    sql_statement: Update = update(User) \
                            .where(User.id == user_id) \
                            .values(**updated_user_info) \
                            .returning(User)

    query_result = session.execute(sql_statement).one()[0]
    user = {k: v for k, v in query_result.__dict__.items() if not k.startswith('_')}

    if user:
        session.commit()

    return user


def remove_user(session: Session, user_id: UUID) -> dict: 
       
    sql_statement: Update = update(User) \
                            .where(and_(
                                User.id == user_id,
                                User.deleted_at.is_(None)) \
                            ) \
                            .values(deleted_at=now_with_timezone()) \
                            .returning(User.id)

    deleted_user_id: UUID = session.scalar(sql_statement)

    if deleted_user_id is not None:
        session.commit()
    else:        
        return {}

    return {'user_id': deleted_user_id}
