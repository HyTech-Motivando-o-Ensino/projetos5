FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD password
ENV MYSQL_DATABASE pj5data
ENV MYSQL_USER user
ENV MYSQL_PASSWORD password

# COPY init.sql /docker-entrypoint-initdb.d/
COPY ddl.sql ./

EXPOSE 3306