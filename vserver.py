"""
Create a server that can receive communication from the twitchbot for game comms
"""
import os,sys
import asyncio
import pickle
import socket
import json
import logging
import vcontroller as vc
import windowfocus as focus
import selectors
# async? one server and client conn but multiple messages

class VServer:
    def __init__(self, port=None):
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = port if port else int(os.environ["GAMEPORT"])



        # Max 2 players
        self.player1 = None
        self.player2 = None

    async def vserve(self):
        #coupling handler and server
        #async with
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.setblocking(False)
            s.settimeout(10)
            s.listen(5) # max backlog
            self.loop = asyncio.get_running_loop()
            # loop = asyncio.get_event_loop()
            #while True:
            #   client, _ = await loop.sock_accept(server)
            #
            #   loop.create_task(self.process_request(data))
            #conn, addr = s.accept()
            conn, add = await self.loop.sock_accept(s) # needs to be non blocking with async def

            with conn:
                print('Ready 2 Game')
                while True:
                    # conn, addr = s.accept() ?? put here to continuously accept requests?
                    #                   (should be one consistent client-server connection per fight so I'm leaning towards no)
                    data = await self.loop.sock_recv(conn, 1024) # max bytes to receive will maybe lower
                    if data:
                        print(f"Incoming request: {data}")
                        # cleaned data incoming
                        # {player1: Player, move_set: LIST}
                        resp = self.process_request(data)
                        if resp:
                            print(f"Outgoing response: {data}")
                            #await self.loop.sock_sendall(conn, resp)
                    await asyncio.sleep(0.5)
        return

    def process_request(self, data):
        # Supporting requests to create_player, overwrite_player, play, getplayername
        # TODO: Return should be a call to some send command
        # essentially is just plugging in a controller
        # self.decoder / self.encoder() ||  json.JSONEncoder() load costs
        data = json.loads(data.decode())
        return_set = {}
        if data['request'] == 'create_player':
            ## create_player; 'player': '<username>'
            #
            return_set['player_controller'] = vc.Controller(data['player'])
            if not self.player1:
                self.player1 = return_set['player_controller']
                response = {'response': 'Assigned player 1'}
            else:
                self.player2 = return_set['player_controller']
                response = {'response': 'Assigned player 2'}
            return response

        # player sends moveset
        #
        elif data['request'] == 'play':
            # first idea was saving and returning the controller obj, but
            # that should all just get handled on the server side
            # {'request':'play'; 'player':'player1'}
            player = data.get('player')
            if player == 'player1':
                self.getgamefocus('Mortal Kombat 11')
                # TODO: Unpause game
                self.player1.parse_moveset(data['moveset'])
            elif player == 'player2':
                self.getgamefocus('Mortal Kombat 11')
                self.player.parse_moveset(data['moveset'])
            else:
                print("This person isn't a player")

            return None

        # todo send some select player data
        # maybe limit the user's first move to select player and I will start the game?

        # overwrite a current player
        elif data['request'] == 'overwrite_player':
            new_controller = vc.Controller(name=data['new_player'])
            if self.player1 and self.player1.name == data['old_player']:
                self.player1 = new_controller
                response = {'response': 'Reassigned player 1'}
            elif self.player2 and self.player2.name == data['old_player']:
                self.player2 = new_controller
                response = {'response': 'Reassigned player 2'}
            else:
                response = {'response': "No players created or none with that name"}

            return response

        # Who is playing
        elif data['request'] == 'getplayername':
            player_name = data['playername']
            if self.player1 and player_name == self.player1.name:
                response = {'response': f'{player_name} is player 1'}
            elif self.player2 and player_name == self.player2.name:
                response = {'response': f'{player_name} is player 2'}
            else:
                response = {'response': f'{player_name} not playing right now'}
        else:
            response = {'response': "Invalid Request"}

        return response


    def getgamefocus(self, name):
        focus.focus_window(name)
        return

    @classmethod
    def getsubprocessenv(cls) -> str:
        return None
        #with open('windows.pickle', 'rb') as p:
        #    return pickle.loads(p)

    @classmethod
    def close(cls):
       # get running processes
       pass

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
        server = VServer(port)
    except IndexError:
        print("Using environment variables")
        server = VServer()
    asyncio.run(server.vserve())
