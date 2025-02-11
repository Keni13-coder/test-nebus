FROM bitnami/pgbouncer:latest

COPY i_docker/pgbouncer.ini /opt/bitnami/pgbouncer/conf/pgbouncer.ini
COPY i_docker/userlist.txt /opt/bitnami/pgbouncer/conf/userlist.txt

EXPOSE 6432
