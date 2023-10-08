# Badge System

## How this project was born
This project was born from the need to create REST APIs for a technical test.<br>
Its evolution is the consequence of my curiosity to always implement new things and improve existing ones, continuously refactoring the project code.<br>
The idea for the project, applied to another area, was given to me by a dear friend and former work colleague, whom I thank for the inspiration and help given to me throughout the development of the project.

## Purpose of the project
The aim of the project was to create APIs as desired, implementing some endpoints and developing some logic in this regard (not just CRUD), making sure to have enough material to start a discussion about it and, possibly, implement features to test my skills (during the technical interview phase).

## Scenario

The managers of a manufacturing company, driven by the desire to improve the management of their employees' attendance both in terms of workplace safety and quality, decide to install a series of badge readers in their company.<br>
Each badge reader identifies a specific access area, limited by a door that can be unlocked both on entry and exit exclusively via a badge, assigned to each employee.

## Description of entities

Taking the scenario described previously as a reference, the main entities can be extrapolated, such as:
- User
- Badge Reader
- Badges

## Relationships between entities
Each user is associated with a badge, and each badge is associated with only one user, so the relationship between User and Badge is one to one.

With the badge, the user must be able to access multiple areas defined by the various badge readers, and, vice versa, a badge reader can allow access to multiple badges, so the relationship between Badge and Badge Reader is many to many.<br>
For this type of relationship, it is necessary to create an associative table, so that the many-to-many relationship between the two entities can be managed correctly.

## Secondary entities
The access information (the user's badge ID, the badge reader that read it, the user's entry date and exit date in/from a specific area) must be able to be saved, making The creation of an "Accesses" entity is required.

The logic that was developed for saving login information is described below.

A user can access and exit only one area at a time, assuming that the entry and exit readings are consequent, having the location constraint where a user cannot clock in to a location and clock in. exited elsewhere.<br>
Making this premise, an _UPSERT_ type logic was adopted;<br>
when a user clocks in, this is saved in the access table, inserting the badge_id, the badge_reader_id and the entry date/time in the same.<br>
When the user clocks in again (with the same badge and at the same badge reader), the access ID is recovered, updating the record's exit date/time information.<br>
In this way, each record collects the information necessary to reconstruct the movements of each user in a simple and intuitive way, giving the possibility of calculating the time spent in each place, the number of accesses made in a specific area, and much other information .

## Project structure
The project has been structured following the best practices for back-end projects.<br>
Since the project is focused on the development of REST APIs, the root folder contains all the project files, consequently subdividing the database, models, schemas and routers.
Each model folder includes all the methods available for its endpoint, calling them accordingly with the CRUD convention. 
```
badge_system
├── .dockerignore
├── .gitignore
├── db
│   ├── data.db
│   └── utils.py
├── docker-compose.yaml
├── Dockerfile
├── main.py
├── models
│   ├── access
│   │   ├── access.py
│   │   ├── create.py
│   │   └── retrieve.py
│   ├── badge
│   │   ├── badge.py
│   │   ├── create.py
│   │   ├── delete.py
│   │   ├── retrieve.py
│   │   ├── update.py
│   │   ├── utils.py
│   │   └── __init__.py
│   ├── badge_reader
│   │   ├── badge_reader.py
│   │   ├── create.py
│   │   ├── delete.py
│   │   ├── retrieve.py
│   │   ├── update.py
│   │   ├── utils.py
│   │   └── __init__.py
│   ├── seed.sql
│   ├── user
│   │   ├── create.py
│   │   ├── delete.py
│   │   ├── retrieve.py
│   │   ├── update.py
│   │   ├── user.py
│   │   ├── utils.py
│   │   └── __init__.py
│   ├── utils.py
│   └── __init__.py
├── README.md
├── requirements.txt
├── routers
│   ├── accesses.py
│   ├── badges.py
│   ├── badge_readers.py
│   ├── users.py
│   └── __init__.py
├── schemas
│   ├── access.py
│   ├── badge.py
│   ├── badge_reader.py
│   ├── user.py
│   └── __init__.py
└── __init__.py

```

## Used technologies
- [SQLite3](https://www.sqlite.org/index.html) as database engine;
- [FastAPI](https://fastapi.tiangolo.com/) as framework to build the APIs;
- [SQLAlchemy](https://www.sqlalchemy.org/) as ORM;
- [Pydantic](https://docs.pydantic.dev/latest/  ) (included in FastAPI) to validate request and response data;
- [ruff](https://docs.astral.sh/ruff/) as code linter.



## Installation

The project can be installed:
- via [virtualenv](#virtual-environment)
- via [Docker](#with-docker) (Dockerfile + CLI)
- via [Docker Compose](#with-docker-compose) (docker-compose.yaml + CLI)

#### Virtual Environment

After downloading the project from GitHub, you need to continue installing the requirements via the command:

```
python -m pip install -r requirements.txt
```

and activate the virtual environment via the command:
```
.\venv\Scripts\activate
```

Once these steps have been completed, you can start the API server using the command:
```
.\venv\Scripts\uvicorn main:app --port 8080
```

Now that the server is up and running, we can proceed with the last step, that is, importing the seed file to have test data in the database.<br>
This last step is <b>not mandatory</b>, but is _recommended_ so as to avoid recreating all the data to test the application.

Open the terminal and type the command:
```
sqlite3 .version
```
and press enter.<br>
If the command correctly returns the version of SQLite installed on your PC, then you can proceed with executing the command:
```
.open [db full file path].db
```
This command will open the database saved on disk and allow us to interact with it.<br>
If sqlite3 is not installed on your PC, follow the guide to install it at this [link](https://www.sqlite.org/download.html).<br>
Once you have opened the database via the SQLite3 CLI, simply launch the command:
```
.read [seed full file path].sql 
```
to import all test data.<br>
To exit the SQLite3 CLI, simply use the command:
```
.quit 
```
#### With Docker

For a faster setup, you can use the <b>Dockerfile</b> with the following commands (to execute in the specified order):

```
docker volume create app-db
docker image build . --tag "badge_system_image"
docker container run -d --name badge_system_container --mount type=volume,source=app-db,destination=/app/models/db -p 8080:8080 badge_system_image
docker container exec -i -t badge_system_container sqlite3 /app/models/db/data.db -init /app/models/seed.sql .quit
```

#### With Docker Compose
For a even faster setup, you can use <b>Docker Compose</b> running the following command:

```
docker compose up -d
```

From this moment you can use the application accessing it though the URL:
```
http://127.0.0.1:8080/
```

For a complete overview of the APIs and to access a playground of the same, just visit the link:
```
http://127.0.0.1:8080/docs
```

<!-- ## Integration with MIT App Inventor

To carry out tests closer to reality, I developed a small application using the no-code MIT App Inventor tool.
The application, once configured via the "Settings" screen, allows you to scan a QR code that identifies an access area, recording the user's access/exit via the "/accesses" endpoint. -->
