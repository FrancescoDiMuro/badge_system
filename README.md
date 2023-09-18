# Badge System

## How this project was born
The managers of a manufacturing company, driven by the desire to improve the management of their employees' attendance both in terms of workplace safety and quality, decide to install a series of badge readers in their company.<br>
Each badge reader identifies a specific access area, limited by a door that can be unlocked both on entry and exit exclusively via a badge, assigned to each employee.

## Purpose of the project
The aim of the project is to give a general idea of how to structure an application that serves its purpose, ideally respecting user requirements and passing a series of validations.

## Used technologies
- [SQLite3](https://www.sqlite.org/index.html) as database engine;
- [FastAPI](https://fastapi.tiangolo.com/) as framework to build the APIs;
- [SQLAlchemy](https://www.sqlalchemy.org/) as ORM;
- [Pydantic](https://docs.pydantic.dev/latest/  ) (included in FastAPI) to validate request and response data;
- [ruff](https://docs.astral.sh/ruff/) as code linter.



## Installation

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
From this moment you can use the application accessing it though the URL:
```
http://127.0.0.1:8080/
```

For a complete overview of the APIs and to access a playground of the same, just visit the link:
```
http://127.0.0.1:8080/docs
```

