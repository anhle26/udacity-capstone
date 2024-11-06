# Motivation for the Project

This project was inspired by the need for a more efficient and user-friendly way to manage movie collections. Many existing solutions are either too complex or lack the features that users truly need. By developing this API, we aim to provide a robust and scalable solution that allows users to easily add, retrieve, update, and delete movie records, all while ensuring secure access through role-based access control (RBAC).

Additionally, this project is part of the Udacity Full Stack Web Developer Nanodegree program, where the goal is to build a comprehensive capstone project that demonstrates mastery of backend development, authentication, and deployment.

## API URL The API is hosted live at: [https://udacity-capstone-0xx5.onrender.com](https://udacity-capstone-0xx5.onrender.com)

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `udacity_capstone_db` database:
```bash
createdb udacity_capstone_db
```
Populate the database using the `capstone_project.psql` file provided. From the folder in terminal run:

```bash
psql udacity_capstone_db < capstone_project.psql
```

### Run the Server

From within the directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.
### RBAC
- Casting assistant permissions:
    "get:actors",
    "get:movies"
- Casting director permissions:
    "get:actors",
    "get:movies",
    "delete:actors",
    "post:actors",
    "patch:actors",
    "patch:movies"
- Executive producer permissions:
    "get:actors",
    "get:movies",
    "delete:actors",
    "delete:movies",
    "post:actors",
    "post:movies",
    "patch:actors",
    "patch:movies"

### Expected endpoints and behaviors

### `GET '/actors'`
- Fetch the list of all actors from the server. 
- Request Arguments: None
- Returns: A list of actor objects containing the attributes id, age, gender and name.


### `POST '/actors'`
- post a new actor to the server.
- Request Arguments: An object containing string attributes including age, gender, and name.


### `PATCH '/actors/<int:actor_id>'`
- Find the actor with the matching ID from the URL and modify that actor's data.
- Request Arguments: An object has at least one of these properties: age, gender, or name.

### `DELETE '/actors/<int:actor_id>'`
- Find and delete the actor whose ID matches the ID in the URL.
- Request Arguments: None


### `GET '/movies'`
- Fetch the list of all movies from the server. 
- Request Arguments: None
- Returns: A list of movie objects containing the attributes id, release date and title.

### `POST '/movies'`
- post a new actor to the server.
- Request Arguments: An object has at least one of these properties: release date and name.

### `PATCH '/movies/<int:movie_id>'`
- Find the actor with the matching ID from the URL and modify that actor's data.
- Request Arguments: An object has at least one of these properties: release date or name.

### `DELETE '/movies/<int:movie_id>'`
- Find and delete the actor whose ID matches the ID in the URL.
- Request Arguments: None
- Returns: An object with an actor_removed property that holds the ID of the recently deleted actor.

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb udacity_capstone_db_test
createdb udacity_capstone_db_test
psql udacity_capstone_db_test < capstone_project.psql
python test_app.py