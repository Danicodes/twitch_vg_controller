"""
A client to communicate with the vserver
"""
import os, sys
import asyncio
import json
import socket
import logging

class VClient:
    def __init__(self, host=None, port=None, loop=None):
        self.HOST = host if host else socket.gethostbyname(socket.gethostname())
        self.PORT = port if port else int(os.environ["GAMEPORT"])
        self.sock = None

        #if loop:
        #    self.loop = loop
        print(loop)

    def start_client(self, loop=None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.settimeout(20)
        #sock.bind(('', self.PORT))

        sock.connect_ex((self.HOST, self.PORT))

        #if not self.loop:
            #self.loop = asyncio.get_running_loop()

        #await self.loop.sock_connect(sock, (self.HOST, self.PORT))
        print("Successfully connected")
        self.sock = sock
        return

    # Should run in a async loop of some kind listening for requests to send?
    def send(self, data: dict):
        try:
            print(f"Sending request {data}")
            self.sock.send(json.dumps(data).encode())
        except:
            e = sys.exc_info()[0]
            print(e)
            breakpoint()
            self.close()
        return

    def close(self):
        self.sock.close()
        return

    async def recv(self):
        # needs to listen for server responses as well
        while True:
            print("Client loop started")
            # listen for some server response
            listen = self.loop.sock_recv(sock, 2048) # create_task
            if listen:
                print(resp)
            await asyncio.sleep(0.5)
        return

if __name__ == '__main__':
    client = VClient()
    client.start_client()

    create_request = {"request":"create_player", "player": "dani"}
    client.send(create_request)
    play_request = {"request": "play", "player": "player1", "moveset": "LUUDDBABABA"}
    client.send(play_request)

    #asyncio.gather(client.send(request), client.recv())
