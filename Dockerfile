FROM python:3.11

RUN mkdir /stock_market
WORKDIR /stock_market

RUN pip3 install pipenv

COPY Pipfile /stock_market
COPY Pipfile.lock /stock_market

RUN pipenv sync --system

COPY . .

WORKDIR /stock_market/stock_market