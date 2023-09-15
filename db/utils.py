from datetime import datetime
from pytz import timezone
from sqlalchemy import Engine, create_engine

from db.models import Base


db_config_params: dict = {'DB_TYPE': 'sqlite',
                          'DB_API': 'pysqlite',
                          'DB_RELATIVE_FILE_PATH': 'db/data.db'}

DB_CONNECTION_STRING: str = '{DB_TYPE}+{DB_API}:///{DB_RELATIVE_FILE_PATH}'.format(**db_config_params)


def db_connect(create_metadata: bool = False, echo: bool = False) -> Engine | None:

    '''Connects to the specified db (SQLite).
    
    Arguments:
     - create_metadata (bool): flag to enable the creation of database metadata
     - echo (bool): flag to enable the printing of debug messages on the console

    Returns:
     - 'sqlalchemy.Engine' in case of success
     - 'None' in case of failure
    '''
    
    # Create the SQLAlchemy engine and metadata (if specified)
    engine: Engine = create_engine(DB_CONNECTION_STRING, echo=echo)
    if create_metadata:
        Base.metadata.create_all(bind=engine)

    return engine if isinstance(engine, Engine) else None


def now_with_timezone(tz: str = 'Europe/Rome'):
    return datetime.now(timezone(tz)).strftime('%Y-%m-%d %H:%M:%S%z')
