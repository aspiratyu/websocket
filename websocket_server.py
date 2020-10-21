import asyncio
import logging
import threading
from multiprocessing import Process,Manager
import task as task
import websockets
from fly import *
from websockets import WebSocketServerProtocol

SERVER = '192.168.0.33'
PORT = 5050
logging.basicConfig(level=logging.INFO)


point = point(1, 1)


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

    async def ws_handler(self, ws:WebSocketServerProtocol, url: str) -> None:
        await self.register(ws)
        try:
            await self.distribute(ws)
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol) -> None:
        async for message in ws:
            print(message)
            #(x, y) = fly.getflycoord(myfly)
        #    await self.send_to_clients(x + " " + y)
            await self.send_to_clients(message)

  #  async def sendflycoord(self, ws: WebSocketServerProtocol) -> None:


  #loop.run_forever()


if __name__ == '__main__':
    myfly = fly(1000, 1000, 100)
    messages_buffer = Manager().list()
    processes =[]

    #serverthread = threading.Thread(target=start())
    #serverthread.start()
    #loop = asyncio.get_event_loop()
    server = Server()
    start_server = websockets.serve(server.ws_handler, SERVER, PORT)
    pServer = Process(target=websockets.serve(server.ws_handler, SERVER, PORT))
    #tasks = [(task,"One",start_server),(task,"Two",myfly.animate())]
    #wait_tasks = asyncio.wait(tasks)
    #loop.run_until_complete(wait_tasks)
    #loop.run_forever(wait_tasks)

    #myfly.start_fly()
    #print(threading.active_count())
    #thread = threading.Thread(target=myfly.animate())
    #thread.start()
    #print("xfsdfsdafs")



