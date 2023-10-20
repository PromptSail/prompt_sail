run:
	docker-compose up --build
	
run-dev:
	cd src && uvicorn app:app --reload --proxy-headers --host 0.0.0.0
	
build:
	docker-compose build
	
precommit:
	pre-commit run --all-files
