from db.utils import db_connect
from db.models import User, BadgeReader, Badge, BadgeReader_Badge
from db.dummy_data import dummy_users, dummy_badge_readers, dummy_badges
from sqlalchemy.orm import Session
from sqlalchemy import select, Select
from operator import itemgetter
from random import randint

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