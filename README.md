# Sportsbook

## Expecifications:

Application builded with:
- Framework: Flask;
- Database: Sqlite3;
- Serializer: Mashmallow;
- Documentation:
    - Swagger for API.
    - Mkdocs to project info.

## Start Project

```shell
# Python path
$ which python3

# Create virtual enviroment
$ virtualenv --python='/usr/bin/python3' .venv

# Activate virtual enviroment
$ source .venv/bin/activate 

# Install requirements
$ make install

# Run project
$ make run
flask run
 * Serving Flask app 'app' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
 * Restarting with watchdog (inotify)
 * Debugger is active!
 * Debugger PIN: 164-808-289

```

## Documentation
I use Mkdocs to create a live documentation. You can acces the documentation online: [link](https://handboy.github.io/sport-book/)

Or run locally:

```shell
# Run and access Mkdocs
$ mkdocs serve
INFO     -  Building documentation...
INFO     -  Cleaning site directory
INFO     -  Documentation built in 0.25 seconds
INFO     -  [18:53:48] Watching paths for changes: 'docs', 'mkdocs.yml'
INFO     -  [18:53:48] Serving on http://127.0.0.1:8000/
INFO     -  [18:54:01] Browser connected: http://127.0.0.1:8000/

# Deploy documentation
$ mkdocs gh-deploy
```

## Tasks
- [X] API CRUD Sport
- [X] API CRUD Event
- [X] API CRUD Selection
- [X] Searching with filters for Sports
- [X] Searching with filters for Events
- [X] Searching with filters for Selections
- [X] When all the selections of a particular event are inactive, the event becomes inactive.
- [X] When all the events of a sport are inactive, the sport becomes inactive
- [X] Sports, events and selections need to be persistently stored (SQLite is allowed)
- [ ] Filters: All (sports/events/selections) with a name satisfying a particular regex
- [ ] Filters: All (sports/events) with a minimum number of active (events/selections) higher than a threshold
- [ ] Filters: Events scheduled to start in a specific timeframe for a specific timezone
- [X] Make File


## Points to Improve
- [ ] Try fix warnings from tests.
- [ ] Add authorization in endpoints.
- [ ] Expecify the error when send data different expected by scheme.
- [ ] Add pagination.
- [ ] Remove code duplication between repositories.
- [ ] Add partial update.
- [ ] Register Api exception.
- [ ] Increase coverage.


## Utils References
- [Install Black](https://marcobelo.medium.com/setting-up-python-black-on-visual-studio-code-5318eba4cd00)
- [Sqlite Datatypes](https://www.sqlite.org/datatype3.html)
- [Marshmallow](https://marshmallow.readthedocs.io/en/stable/index.html)
- [Flask Apispec](https://flask-apispec.readthedocs.io/en/latest/usage.html)
- [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)