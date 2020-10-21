import asyncio
import logging
import websockets
from websockets import WebSocketServerProtocol

logging.basicConfig(level=logging.INFO)
SERVER = '192.168.0.174'
PORT = "5050"
websocket_resourse_url = f"ws://{SERVER}:{PORT}"


async def handler(websocket: WebSocketServerProtocol) -> None:
    consumer_task = asyncio.ensure_future(
        consumer_handler(websocket))
    producer_task = asyncio.ensure_future(
        producer_handler(websocket))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()


async def consumer_handler(websocket: WebSocketServerProtocol):
    async for message in websocket:
        await consumer(message)


async def consumer(message):
    log_message(message)


async def producer_handler(websocket: WebSocketServerProtocol):
    while True:
        message = await producer()
        await websocket.send(message)


async def producer() -> str:
    return input()


def log_message(message: str) -> None:
    logging.info(f"Message:{message}")


async def connect():
    async with websockets.connect(websocket_resourse_url) as ws:
        await handler(ws)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect())
    loop.run_forever()
