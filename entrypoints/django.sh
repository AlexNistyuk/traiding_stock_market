#!/bin/bash

python stock_market/manage.py migrate
python stock_market/manage.py runserver $WEB_CONTAINER_HOST:$WEB_PORT
