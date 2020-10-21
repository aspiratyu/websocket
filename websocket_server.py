import asyncio
import logging
import threading
from multiprocessing import Process,Manager
import task as task
import websockets
from fly import *
from websockets import WebSocketServerProtocol

SERVER = '192.168.0.174'
PORT = 5050
logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        self.clients.remove(ws)
        await ws.close(1000, "normal closure")
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str) -> None:
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def ws_handler(self, ws: WebSocketServerProtocol, url: str) -> None:
        await self.register(ws)
        try:
            await self.distribute(ws)
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol) -> None:
        async for message in ws:
            print(message)
            #(x, y) = fly.getflycoord(myfly)
            #await self.send_to_clients(x + " " + y)
            await self.send_to_clients(message)

  #  async def sendflycoord(self, ws: WebSocketServerProtocol) -> None:


  #loop.run_forever()


if __name__ == '__main__':
    myfly = fly(1000, 1000, 100)
    server = Server()
    start_server = websockets.serve(server.ws_handler, SERVER, PORT)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_until_complete(myfly.animate())
    loop.run_forever()

