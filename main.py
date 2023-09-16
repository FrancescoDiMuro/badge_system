from db.utils import db_connect
from db.models import User, BadgeReader, Badge, BadgeReader_Badge, Access
from db.dummy_data import dummy_users, dummy_badge_readers, dummy_badges
from sqlalchemy.orm import Session
from sqlalchemy import select, update, and_
from uuid import UUID, uuid4
from sqlalchemy.exc import NoResultFound
from db.utils import now_with_timezone


if __name__ == '__main__':

    # Connect to the database
    engine = db_connect(create_metadata=True, echo=True)
    if engine is not None:
               
        # Create the session
        with Session(bind=engine) as session:

            # badge_ids = session.execute(select(Badge.id)).all()           
            # TEST_BADGE_ID = badge_ids[randint(0, len(badge_ids) - 1)][0]

            # badge_reader_ids = session.execute(select(BadgeReader.id)).all()            
            # TEST_BADGE_READER_ID = badge_reader_ids[randint(0, len(badge_reader_ids) - 1)][0]

            TEST_BADGE_ID: UUID = UUID('e3cc0cc89e234ae69b0e02f391428323')
            TEST_BADGE_READER_ID: UUID = UUID('7979a93fd0ff45b588845a4d38a6f2da')


            # Check if User has already badged to a specific BadgeReader
            sql_statement = select(Access.id) \
                            .where(and_( \
                                Access.badge_id == TEST_BADGE_ID),
                                Access.badge_reader_id == TEST_BADGE_READER_ID,
                                Access.out_timestamp.is_(None))
                        
            try:
                # Using 'execute' instead of 'scalars' to get advantage of being able to obtain
                # the values of selected columns
                access_id = session.execute(sql_statement).one()[0]
            except NoResultFound:
                
                # Simulate access from user
                new_access = {
                    'id': uuid4(),
                    'badge_id': TEST_BADGE_ID,
                    'badge_reader_id': TEST_BADGE_READER_ID
                }

                # Create the new access
                access = Access(**new_access)
                session.add(access)
                session.commit()

            else:

                # Create the update statement
                sql_statement = update(Access) \
                                .where(Access.id == access_id) \
                                .values(out_timestamp=now_with_timezone())
                
                session.execute(sql_statement)
                session.commit()
                