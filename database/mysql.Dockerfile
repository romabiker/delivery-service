FROM mariadb:10.8

ENV MYSQL_USER=admin
ENV MYSQL_PASSWORD=changethis
ENV MYSQL_DATABASE=delivery
ENV MYSQL_ROOT_PASSWORD=changethis

COPY ./my.cnf /etc/mysql/conf.d/my.cnf

# CMD: []
