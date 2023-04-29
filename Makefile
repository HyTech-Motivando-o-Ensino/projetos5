run-dev:
	docker-compose up --build -d

create-tables:
	docker exec mysql_db /bin/sh -c 'mysql -u user -ppassword < ddl.sql'