from sqlalchemy.orm import Session
from sqlalchemy import Select, select, and_
from db.models import User
from uuid import UUID

def read_users(session: Session, name_like: str, surname_like: str, email_like: str) -> list[dict]:

    users: list = []
    
    sql_statement: Select = select(User) \
                            .where(and_( \
                                User.deleted_at.is_(None),
                                User.name.like(name_like),
                                User.surname.like(surname_like),
                                User.email.like(email_like))) \
                            .order_by(User.created_at)          
    
    query_result = session.execute(sql_statement).all()
    for record in query_result:
        users.append({k: v for k, v in record[0].__dict__.items() if not k.startswith('_')})    

    return users


def read_user_by_id(session: Session, user_id: UUID) -> dict:

    user: dict = {}
    
    sql_statement: Select = select(User) \
                            .where(and_( \
                                User.deleted_at.is_(None),
                                User.id == user_id)) \
                            .order_by(User.created_at)             
    
    query_result = session.execute(sql_statement).one()
    
    user = {k: v for k, v in query_result[0].__dict__.items() if not k.startswith('_')}

    return user