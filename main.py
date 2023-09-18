from fastapi import FastAPI
from routers import users, badge_readers, badges, accesses


APP_DESCRIPTION = '''### Monitor access with a badge control system through REST APIs.
<br>
### Introduction

This APIs let you create and configure users, badge readers, badges and monitor accesses in your plant area.

### Configured endpoints
A list of configured endpoints can be found below.

### Credits
- Developer: Francesco Di Muro - [Work Portfolio (IT)](https://www.francescodimuro.com/) | [Work Portfolio (EN)](https://www.en.francescodimuro.com/)
'''

APP_METADATA: dict = {'title': 'Badge System',
                    'description': APP_DESCRIPTION}

ROOT_ENDPOINT_METADATA: dict = {
    'summary': 'Root endpoint', 
    'description': 'This is the root endpoint of the REST API server.', 
    'response_model': None,
    'tags': ['root']
    }


app = FastAPI(**APP_METADATA)

app.include_router(users.router)
app.include_router(badge_readers.router)
app.include_router(badges.router)
app.include_router(accesses.router)

@app.get('/', **ROOT_ENDPOINT_METADATA)
async def get_root():
    return {'message': 'Welcome to Badge System!'}



