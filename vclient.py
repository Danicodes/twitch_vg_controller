"""
A client intended to run on WSL2 and interface with a server running in powershell
on Windows.
"""
import os, sys
import asyncio
import json
import socket
import logging

# TODO: (A) Either redo the script with aihttp/websocket communication to
#           handle multiple buffer pileup on the server side
#       (B) implement a method to run within the bot, to let us async'ly recieve
#       responses from the server (create_task from bot?)
#

class VClient:
    def __init__(self, host=None, port=None):
        self.HOST = '127.0.0.1' # localhost/loopback addr
        self.PORT = port if port else int(os.environ["GAMEPORT"])
        self.sock = None

    def start_client(self, loop=None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.settimeout(20)
        sock.connect_ex((self.HOST, self.PORT))

        #if not self.loop:
            #self.loop = asyncio.get_running_loop()

        #await self.loop.sock_connect(sock, (self.HOST, self.PORT))
        print("Successfully connected")
        self.sock = sock
        return

    def send(self, data: dict):
        try:
            print(f"Sending request {data}")
            self.sock.send(json.dumps(data).encode())
        except : # Just anything right now
            e = sys.exc_info()[0]
            print(e)
            raise
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
    # Testing a constant connection
    client = VClient()
    client.start_client()

    create_request = {"request":"create_player", "player": "dani"}
    client.send(create_request)

    while True:
        moveset = input("play moveset?")
        play_request = {"request": "play", "player": "player1", "moveset": moveset}
        client.send(play_request)

    #asyncio.gather(client.send(request), client.recv())
