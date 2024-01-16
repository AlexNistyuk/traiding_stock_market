import asyncio
import json

from aiokafka import AIOKafkaConsumer
from brokers.tasks import MessageBrokerHandler

from stock_market.settings import CONSUMER_GROUP, KAFKA_TOPIC, KAFKA_URL


class Consumer:
    async def __aenter__(self):
        self.consumer = AIOKafkaConsumer(
            KAFKA_TOPIC,
            CONSUMER_GROUP,
            bootstrap_servers=KAFKA_URL,
        )
        await self.consumer.start()

        self.message_handler = MessageBrokerHandler()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.consumer.stop()

    async def start(self):
        async for msg in self.consumer:
            tickers: list[dict] = json.loads(msg.value)

            self.message_handler.handle.delay(tickers)


async def consume():
    async with Consumer() as consumer:
        await consumer.start()


if __name__ == "__main__":
    asyncio.run(consume())
