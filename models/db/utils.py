from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base


db_config_params: dict = {'DB_TYPE': 'sqlite',
                          'DB_API': 'pysqlite',
                          'DB_RELATIVE_FILE_PATH': 'models/db/data.db'}

DB_CONNECTION_STRING: str = '{DB_TYPE}+{DB_API}:///{DB_RELATIVE_FILE_PATH}'.format(**db_config_params)

engine: Engine = create_engine(DB_CONNECTION_STRING, 
                               connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine)

def get_db() -> SessionLocal:
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()    
