## Структура Базы данных
![docs](./docs/entity.drawio.svg)

## Структура классов API
![docs](./docs/classes-API.drawio.svg)

## Структура классов брокера
![docs](./docs/classes-broker.drawio.svg)

## Запуск бд
```sh
docker build -t my-postgis -f i_docker/postgres.dockerfile .
docker run -d \
  --name my-postgis \
  --env-file .env \
  -v postgis_data:/var/lib/postgresql/data \
  -p 5433:5432 \
  --network postgres-network \
  my-postgis

docker build -t my-pgbouncer -f i_docker/pgbouncer.dockerfile .
docker run -d \
  --name my-pgbouncer \
  --network=postgres-network \
  --env-file .env \
  -p 6432:6432 \
  my-pgbouncer
```