### Launch in dev mode (local):

* Set environment variables
* FLASK_APP=run.py flask run

### Launch in prod mode:
* Set environment variables
* `uwsgi --http :5000 --module run:app`
* http://localhost:5000/ should render

### Alembic migrations

* Alemebic is initialized with `alembic init alembic` (once done it creates alembic 
folder that contains migrations and no need to re-do the command)
* To create (the first or next's) migration: `alembic revision --autogenerate -m "Initial migration"`
* At each migration created we apply it with `alembic upgrade head` (if it is the first time, it will create 
`main_engine.db` in the root of the project, otherwise it will update the file).
