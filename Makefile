BUILD_SHA ?= $(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")

run:
	docker-compose up

run-build:
	docker-compose -f docker-compose-build.yml up --build
	
run-dev:
	cd backend/src && uvicorn app:app --reload --proxy-headers --host 0.0.0.0
	
test: 
	cd backend/src && pytest ../tests
	
test-windows:
	 @set DATABASE_NAME=prompt_sail_test&& cd backend\src && pytest ..\tests -vv
 
perf-tests:
	cd backend/perf_tests && locust --config locust.conf

build:
	docker-compose -f docker-compose-build.yml build --build-arg BUILD_SHA=$(BUILD_SHA)

build-ui:
	docker-compose -f docker-compose-build.yml build --build-arg BUILD_SHA=$(BUILD_SHA) promptsail-ui

build-backend:
	docker-compose -f docker-compose-build.yml build --build-arg BUILD_SHA=$(BUILD_SHA) promptsail-backend
	
format:
	pre-commit run --all-files
	
heroku:
	heroku container:push web --arg BUILD_SHA=$(BUILD_SHA) -a promptsail
	heroku container:release web -a promptsail
