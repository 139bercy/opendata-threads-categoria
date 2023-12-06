install:
	pip install -r requirements.txt
	pip install -e .

# Docker compose
up:
	docker compose up --build -d

down:
	docker compose down --remove-orphans -v

db:
	docker exec -it app-db /bin/bash

coverage:
	pytest --cov=. && coverage html

## Dev

todo:
	grep -r "TODO" src tests
