import schemas.access
import sqlalchemy.sql.functions as sqlfuncs
from models.access.access import Access
from models.utils import get_fields_from_model
from sqlalchemy.orm import Session
from sqlalchemy import Select, select, and_
from uuid import UUID

def read_accesses(session: Session, in_timestamp_min: str, in_timestamp_max: str,
                  badge_id: UUID, badge_reader_id: UUID) -> list[schemas.access.Access]:
  
    accesses: list = []

    if in_timestamp_min == '' or in_timestamp_max == '':
        
        sql_statement = select(sqlfuncs.min(Access.in_timestamp).label('in_timestamp_min'),
                               sqlfuncs.max(Access.in_timestamp).label('in_timestamp_max'))                
        
        in_timestamp_min, in_timestamp_max = session.execute(sql_statement).all()[0]
    
    sql_statement: Select = select(Access) \
                            .where(
                                and_(
                                        Access.in_timestamp.between(in_timestamp_min, in_timestamp_max),
                                        Access.badge_id == badge_id if badge_id else True,
                                        Access.badge_reader_id == badge_reader_id if badge_reader_id else True
                                    )
                                ) \
                            .order_by(Access.in_timestamp)
        
    print(sql_statement)
    
    query_result = session.scalars(sql_statement).all()

    for model in query_result:
        model_fields = get_fields_from_model(model)
        accesses.append(schemas.access.Access(**model_fields))

    return accesses