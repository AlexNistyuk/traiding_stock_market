#!/bin/bash

cd stock_market

celery -A stock_market worker -l INFO -Q $CELERY_QUEUE
