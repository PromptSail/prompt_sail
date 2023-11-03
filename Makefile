run:
	docker-compose up --build
	
run-dev:
	cd src && uvicorn app:app --reload --proxy-headers --host 0.0.0.0
	
test: 
	cd src && pytest

build:
	docker-compose build
	
precommit:
	pre-commit run --all-files
	
heroku:
	heroku container:push web -a promptsail
	heroku container:release web -a promptsail
