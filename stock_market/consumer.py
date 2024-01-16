import asyncio
import json

import aiohttp
from aiokafka import AIOKafkaConsumer

from stock_market.settings import (
    CONSUMER_GROUP,
    KAFKA_ENDPOINT,
    KAFKA_TOPIC,
    KAFKA_URL,
    WEB_HOST,
    WEB_PORT,
)


class Consumer:
    url = f"http://{WEB_HOST}:{WEB_PORT}{KAFKA_ENDPOINT}"
    headers = {"Content-Type": "application/json"}

    async def __aenter__(self):
        self.consumer = AIOKafkaConsumer(
            KAFKA_TOPIC,
            CONSUMER_GROUP,
            bootstrap_servers=KAFKA_URL,
        )
        await self.consumer.start()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.consumer.stop()

    async def start(self):
        async for msg in self.consumer:
            tickers: list[dict] = json.loads(msg.value)

            await self.__send_tickers(tickers)

    async def __send_tickers(self, tickers: list[dict]):
        async with aiohttp.ClientSession() as session:
            await session.put(url=self.url, data=tickers, headers=self.headers)


async def consume():
    async with Consumer() as consumer:
        await consumer.start()


if __name__ == "__main__":
    asyncio.run(consume())
