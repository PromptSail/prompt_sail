BUILD_SHA ?= $(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")

run:
	docker-compose up
	
run-dev:
	cd backend/src && uvicorn app:app --reload --proxy-headers --host 0.0.0.0
	
test: 
	cd backend/src && pytest ../tests

build:
	docker-compose build --build-arg BUILD_SHA=$(BUILD_SHA)
	
format:
	pre-commit run --all-files
	
heroku:
	heroku container:push web --arg BUILD_SHA=$(BUILD_SHA) -a promptsail
	heroku container:release web -a promptsail
