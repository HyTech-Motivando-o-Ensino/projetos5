up:
	docker-compose up --build -d

down:
	docker-compose down

create-tables:
	docker exec mysql_db /bin/sh -c 'mysql -u user -ppassword < ddl.sql'

stop:
	docker-compose stop

reset-db:
	docker volume rm projetos5_db_created
	docker volume rm projetos5_mysqldata