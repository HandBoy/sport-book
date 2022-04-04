SETTINGS := develop

help: 		## Show this help.
	@echo "Please use \`make <target>' where <target> is one of"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?##"}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install:	## Run command to install requirements.
	pip install -r requirements/dev.txt

db:			## Create and populate database
	flask init-db

run:		## Run the project.
	flask run

doc:		## Run mkdocs documentation.
	mkdocs serve

test: 		## Run command test.
	pytest

routes:	## Run migrate django command.
	flask routes

venv-path:	## Show The path of the virtual env activated.
	echo $VIRTUAL_ENV

clean:		## clean files
	-rm -rf htmlcov
	-rm -rf .coverage
	-rm -rf .pytest_cache
	-rm -rf __pycache__
	-rm -rf *.pyc
