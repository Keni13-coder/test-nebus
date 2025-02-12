## Краткое описание проекта
Структура проекта построена для event-sourcing с разделением CQRS.
3 главные директории:
- src/api - API
- src/shared - общие сущности
- src/stream - stream-события (брокер не используется, так как нет необходимости)

Так как нет команд на изменения состояния, то не использовал брокера
Основная сущность запроса Query, который содержит в себе команды и запросы к базе данных.
Так как запросы на получение данных должны быть синхронными в концепции CQRS то вызовы происходят в api (а не stream).
Управление и поставку данных в Query отвечает Operation.
Существует один endpoint для запроса данных, он обладает динамикой запросов.
Для доступа к данным используется PgBouncer and Postgres.


## Структура Базы данных
![docs](./docs/entity.drawio.svg)

## Структура классов API
![docs](./docs/classes-API.drawio.svg)

## Структура классов брокера
![docs](./docs/classes-broker.drawio.svg)

## Запуск бд
```sh
создайте network

docker build -t my-postgis -f i_docker/postgres.dockerfile .
docker run -d \
  --name my-postgis \
  --env-file .env \
  -v postgis_data:/var/lib/postgresql/data \
  -p 5433:5432 \
  --network postgres-network \
  my-postgis

создайте userlist.txt

docker build -t my-pgbouncer -f i_docker/pgbouncer.dockerfile .
docker run -d \
  --name my-pgbouncer \
  --network=postgres-network \
  --env-file .env \
  -p 6432:6432 \
  my-pgbouncer
```

## Запуск API
```sh
создать ключ для шифрования
создайте network
>>> from src.api.security.security import generate_signature
>>> print(generate_signature())


docker build -t my-api -f i_docker/api.dockerfile .
docker run -d \
  --name my-api \
  --network=postgres-network \
  --env-file .env \
  -p 8000:8000 my-api
```