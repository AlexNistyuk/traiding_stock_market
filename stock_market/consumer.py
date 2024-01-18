import asyncio

import aiohttp
from aiokafka import AIOKafkaConsumer
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from stock_market.settings import (
    CONSUMER_GROUP,
    HTTP_AUTH_KEYWORD,
    KAFKA_EMAIL,
    KAFKA_ENDPOINT,
    KAFKA_PASSWORD,
    KAFKA_TOPIC,
    KAFKA_URL,
    KAFKA_USERNAME,
    LOGIN_ENDPOINT,
    REFRESH_ENDPOINT,
    REGISTER_ENDPOINT,
    WEB_URL,
)


class Consumer:
    kafka_endpoint = f"{WEB_URL}{KAFKA_ENDPOINT}"

    async def __aenter__(self):
        self.consumer = AIOKafkaConsumer(
            KAFKA_TOPIC,
            CONSUMER_GROUP,
            bootstrap_servers=KAFKA_URL,
        )
        await self.consumer.start()

        self.kafka_auth = KafkaAuth()
        await self.kafka_auth.start()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.consumer.stop()

    async def start(self):
        async for msg in self.consumer:
            await self.__send_message(msg.value)

    async def __send_message(self, data):
        async with aiohttp.ClientSession() as session:
            for _ in range(2):
                response = await session.put(
                    url=self.kafka_endpoint,
                    data=data,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"{HTTP_AUTH_KEYWORD} {self.kafka_auth.access_token}",
                    },
                )

                if response.status == HTTP_401_UNAUTHORIZED:
                    await self.kafka_auth.refresh()

                    continue
                break


class KafkaAuth:
    """Register, login and refresh tokens for kafka user"""

    register_endpoint = f"{WEB_URL}{REGISTER_ENDPOINT}"
    login_endpoint = f"{WEB_URL}{LOGIN_ENDPOINT}"
    refresh_endpoint = f"{WEB_URL}{REFRESH_ENDPOINT}"
    access_token: str = None
    refresh_token: str = None

    async def start(self):
        await self.__register()
        await self.__login()

    async def refresh(self):
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url=self.refresh_endpoint,
                data={
                    "refresh_token": self.refresh_token,
                },
            )

            await self.__set_tokens(response)

    async def __register(self):
        async with aiohttp.ClientSession() as session:
            await session.post(
                url=self.register_endpoint,
                data={
                    "email": KAFKA_EMAIL,
                    "username": KAFKA_USERNAME,
                    "password": KAFKA_PASSWORD,
                },
            )

    async def __login(self):
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url=self.login_endpoint,
                data={
                    "username": KAFKA_USERNAME,
                    "password": KAFKA_PASSWORD,
                },
            )

            await self.__set_tokens(response)

    async def __set_tokens(self, response):
        if response.status == HTTP_200_OK:
            response_data = await response.json()

            self.access_token = response_data["access_token"]
            self.refresh_token = response_data["refresh_token"]


async def consume():
    async with Consumer() as consumer:
        await consumer.start()


if __name__ == "__main__":
    asyncio.run(consume())
