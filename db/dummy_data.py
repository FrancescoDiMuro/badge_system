from uuid import UUID, uuid4

dummy_users: list[dict] = [
    {
        'id': uuid4(),
        'name': 'Mario',
        'surname': 'Rossi',
        'email': 'mario.rossi@somedomain.com',
        'phone': '+391234567890'
    },
    {
        'id': uuid4(),
        'name': 'Giovanni',
        'surname': 'Verdi',
        'email': 'giovanni.verdi@somedomain.com',
        'phone': '+390000000000'
    },
    {
        'id': uuid4(),
        'name': 'Francesco',
        'surname': 'Di Muro',
        'email': 'dimurofrancesco@virgilio.it',
        'phone': '+393801234567'
    }
]

dummy_badge_readers: list[dict] = [
    {
        'id': uuid4(),
        'ip_address': '192.168.150.10',
        'location': 'Ingresso principale'
    },
    {
        'id': uuid4(),
        'ip_address': '192.168.150.11',
        'location': 'Officina'
    },
    {
        'id': uuid4(),
        'ip_address': '192.168.150.12',
        'location': 'Manifattura'
    }
]

dummy_badges: list[dict] = [
    {
        'id': uuid4(),
        'code': '1234',
        'user_id': ''
    },
    {
        'id': uuid4(),
        'code': '5678',
        'user_id': ''
    },
    {
        'id': uuid4(),
        'code': '9012',
        'user_id': ''
    },
]