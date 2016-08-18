## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).  Also, install the [Heroku Toolbelt](https://toolbelt.heroku.com/) and [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ cd jennifer-admin

$ pip install -r requirements.txt

$ createdb jennifer
$ psql jennifer -c "CREATE ROLE jenniferadmin PASSWORD 'jennifer-db-letmein' SUPERUSER CREATEDB CREATEROLE INHERIT LOGIN;"

$ export DJANGO_SETTINGS_MODULE='core.settings.local'
$ python manage.py migrate
$ python manage.py collectstatic
$ python manage.py createsuperuser

```


To run server locally on
[localhost:8000](http://localhost:8000/).

```sh
$ python manage.py runserver
```

Alternatively, you can run on heroku locally
```sh
$ heroku local
```
Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
