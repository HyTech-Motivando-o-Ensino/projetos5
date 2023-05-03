up:
	docker-compose up --build

down:
	docker-compose down

down-reset:
	docker-compose down -v

stop:
	docker-compose stop

reset-db:
	docker volume rm projetos5_db_created
	docker volume rm projetos5_mysqldata