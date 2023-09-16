from utils import db_connect
from models import User, BadgeReader, Badge, BadgeReader_Badge, Access
from dummy_data import dummy_users, dummy_badge_readers, dummy_badges
from sqlalchemy.orm import Session
from sqlalchemy import select, update, and_, Select
from operator import itemgetter
from random import randint
from uuid import UUID, uuid4
from sqlalchemy.exc import NoResultFound
from db.utils import now_with_timezone

# Connect to the database
engine = db_connect(create_metadata=True, echo=True)
if engine is not None:
            
    # Create the session
    with Session(bind=engine) as session:
        
        # ----- Dummy Users -----            
        test_users: list[User] = [User(**dummy_user) for dummy_user in dummy_users]

        # Adding data to the session
        session.add_all(test_users)
        
        # Committing changes to the db
        session.commit()

        
        # ----- Dummy Badge Readers -----            
        test_badge_readers: list[BadgeReader] = [BadgeReader(**dummy_badge_reader) for dummy_badge_reader in dummy_badge_readers]

        # Adding data to the session
        session.add_all(test_badge_readers)
        
        # Committing changes to the db
        session.commit()

        users_ids = session.scalars(select(User.id))
        users_ids = [i for i in users_ids]

        sql_statement: Select = select(BadgeReader).order_by(BadgeReader.ip_address)
        test_badge_readers = session.scalars(sql_statement).all()           
        
        # ----- Dummy Badges -----
        for i, dummy_badge in enumerate(dummy_badges):
            dummy_badge['user_id'] = users_ids[i]
        
        test_badges: list[Badge] = [Badge(**dummy_badge) for dummy_badge in dummy_badges]

        badge_readers: list[BadgeReader] = []
        
        for test_badge in test_badges:
            rng = list(range(randint(1, len(test_badge_readers))))                                        
            badge_readers = list(itemgetter(*rng)(test_badge_readers))                

            for badge_reader in badge_readers:
                association_record = BadgeReader_Badge()
                association_record.badge_reader = badge_reader
                test_badge.badge_readers.append(association_record)
                
        # Adding data to the session
        session.add_all(test_badges)
        
        # Committing changes to the db
        session.commit()

        # badge_ids = session.execute(select(Badge.id)).all()           
        # TEST_BADGE_ID = badge_ids[randint(0, len(badge_ids) - 1)][0]

        # badge_reader_ids = session.execute(select(BadgeReader.id)).all()            
        # TEST_BADGE_READER_ID = badge_reader_ids[randint(0, len(badge_reader_ids) - 1)][0]

        TEST_BADGE_ID: UUID = UUID('4391ddd0f82b444aa7328dab681cc153')
        TEST_BADGE_READER_ID: UUID = UUID('daf39b1e4ca240f3a808614155a7fe81')


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