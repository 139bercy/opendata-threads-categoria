# Docker compose
up:
	docker compose up --build -d

down:
	docker compose down --remove-orphans -v

db:
	docker exec -it app-db /bin/bash /usr/bin/psql -U postgres -d app-db