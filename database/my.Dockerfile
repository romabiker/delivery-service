FROM mariadb:10.8

COPY ./my.cnf /etc/mysql/conf.d/my.cnf
COPY ./init.sh /docker-entrypoint-initdb.d
RUN sed -i 's/\r$//g' /docker-entrypoint-initdb.d/init.sh
RUN chown -R mysql:mysql /docker-entrypoint-initdb.d/init.sh
