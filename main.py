from db.utils import db_connect
from db.models import Users, BadgeReaders, Badges, BadgeReaders_Badges
from sqlalchemy.orm import Session
from uuid import uuid4, UUID


if __name__ == '__main__':

    # Create the engine for SQLAlchemy
    engine = db_connect(create_metadata=True, echo=True)
    if engine is not None:
               
        # Create Session
        # Session = sessionmaker(bind=engine)

        with Session(bind=engine) as session:

            new_user: dict = {'id': uuid4(),
                        'name': 'Giovanni',
                        'surname': 'Verdi',
                        'email': 'giovanni.verdi@somedomain.com',
                        'phone': '+391234567890'
                        }
            
            u = Users(**new_user)
            session.add(u)
            session.commit()            
        
            badge_reader: dict = {'id': uuid4(),
                                  'ip_address': '192.168.150.11',
                                  'location': 'Officina'}
            
            br = BadgeReaders(**badge_reader)
            # br.__dict__.get('id')
            
            session.add(br)
            session.commit()

            badge: dict = {'id': uuid4(),
                           'code': '5678',
                           'user_id': UUID('d844b4f8f96c459ca89d4f99a8445c5d')}
            
            # p = Parent()
            # a = Association(extra_data="some data")
            # a.child = Child()
            # p.children.append(a)


            b = Badges(**badge)
            brb = BadgeReaders_Badges()
            brb.badge_reader = br
            print(f'{brb.badge_reader.__dict__=}')
            b.badge_readers.append(brb)
            
            session.add(b)
            session.commit()
