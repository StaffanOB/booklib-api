#!/bin/sh
# name: docker-entry-point
# Description: Runs when container sterts

# Run database migration
flask db upgrade

# Run webserver
exec gunicorn --bind 0.0.0.0:5000 "app:create_app()"
