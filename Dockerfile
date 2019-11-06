FROM docker.io/python:3-alpine

LABEL org.label-schema.name="Healthchecks" \
      org.label-schema.description="Basic intallation of Healthchecks" \
      org.label-schema.schema-version="1.0"

HEALTHCHECK CMD curl -f http://localhost:8080/ || exit 1
ENV PYTHONUNBUFFERED=1

ADD requirements.txt /healthchecks/requirements.txt

WORKDIR /healthchecks

RUN apk add --no-cache tzdata gcc g++ mariadb-dev mariadb-connector-c musl-dev libffi libffi-dev mariadb-client openssl postgresql-dev \
    && ln -s /usr/share/zoneinfo/US/Eastern /etc/localtime \
    # circumvent a bug in pip 19.0.1
    && pip install --upgrade pip \
    && pip install psycopg2-binary \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del gcc mariadb-dev musl-dev libffi-dev postgresql-dev

ADD . /healthchecks
RUN cp docker/local_settings.py hc/. \
    && python manage.py collectstatic --noinput \
    && python manage.py compress

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "hc.wsgi:application", "--log-config", "docker/gunicorn-logging.conf"]
