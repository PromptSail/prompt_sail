BUILD_SHA ?= $(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")

run:
	docker-compose up
	
run-dev:
	cd src && uvicorn app:app --reload --proxy-headers --host 0.0.0.0
	
test: 
	cd src && pytest

build:
	docker-compose build --build-arg BUILD_SHA=$(BUILD_SHA)
	
precommit:
	pre-commit run --all-files
	
heroku:
	heroku container:push web -a promptsail
	heroku container:release web -a promptsail
