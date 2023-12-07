FROM python:3.11

RUN mkdir /stock_market
WORKDIR /stock_market

RUN pip3 install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv sync --system

COPY . .
