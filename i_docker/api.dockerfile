FROM python:3.12-alpine

WORKDIR /app/

ENV INSTALL_DEV=true

# Устанавливаем необходимые пакеты для сборки shapely
RUN apk update && apk add --no-cache \
    bash \
    gcc \
    musl-dev \
    geos \
    geos-dev

RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_VIRTUALENVS_IN_PROJECT=false
ENV POETRY_PYTHON=/usr/local/bin/python
COPY ../. .

RUN poetry lock
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

ENV WORKERS=4
ENV HOST=0.0.0.0
ENV PORT=8000
ENV LOG_LEVEL=info


CMD ["sh", "-c", "poetry run gunicorn --workers $WORKERS --worker-class uvicorn.workers.UvicornWorker --bind $HOST:$PORT --log-level $LOG_LEVEL 'src.api.main:app'"]