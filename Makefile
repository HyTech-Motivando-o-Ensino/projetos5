run:
	docker-compose up --build

down:
	docker-compose down

down-reset:
	docker-compose down -v

stop:
	docker-compose stop

makemigrations:
	docker exec api python manage.py makemigrations

migrate:
	docker exec api python manage.py migrate