#!/bin/bash
NAME="SITENAME"
USER=USERNAME
WORKERS=2
DJANGODIR=/data/www/SITENAME
DJANGO_WSGI_MODULE=${NAME}.wsgi
PID_PATH=/tmp/gunicorn.${NAME}.pid

cd ${DJANGODIR}/source

exec ../virtualenv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --user $USER \
    --pid $PID_PATH \
    --workers $WORKERS \
    --bind=unix:/tmp/SITENAME.socket \
    --log-level=info \
    --access-logfile=${DJANGODIR}/logs/gunicorn.access.log \
    --error-logfile=${DJANGODIR}/logs/gunicorn.error.log \