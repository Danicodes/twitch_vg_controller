"""
A server script that receives communication from the twitch-bot via an instance of the vclient
and manages the creation, deletion and button input for 1 to 2 player controllers
"""
import os,sys
import asyncio
import socket
import json
import logging
import vcontroller as vc
import windowfocus as focus

# TODO:
# (A) Can we figure out how to launch this from the bot (not using subprocess
#       because it messes with Neovim settings)
# (A-2) Restarting the server in an automatic way

class VServer:
    def __init__(self, port=None):
        self.HOST = '127.0.0.1' # localhost works!
        self.PORT = port if port else int(os.environ["GAMEPORT"])

        # Max 2 players
        self.player1 = None
        self.player2 = None

        self.loop = asyncio.get_running_loop()

    async def vserve(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.setblocking(False)
            s.settimeout(10)
            s.listen(1) # max backlog of *connection* requests - 1 or 0

            conn, add = await self.loop.sock_accept(s)

            with conn:
                print('Ready 2 Game')
                while True:
                    data = await self.loop.sock_recv(conn, 1024) # max bytes to receive PER request
                    if data:
                        print(f"Incoming request: {data}")
                        # Assume cleaned data incoming, {player: player1, move_set: LIST}
                        # Create task immediately so we (hopefully) don't end up with a buffer backlog
                        resp = self.loop.create_task(self.process_request(data))
                        if resp:
                            print(f"Outgoing response: {data}")
                            #await self.loop.sock_sendall(conn, resp) # recv not implemented for this
                    await asyncio.sleep(0.5)
        return

    async def process_request(self, data):
        # Supporting requests to create_player, overwrite_player, play, getplayername
        # TODO: Return should be a call to some send command
        # essentially is just plugging in a controller
        # self.decoder / self.encoder() ||  json.JSONEncoder() load costs
        await asyncio.sleep(0)
        try:
            data = json.loads(data.decode())
        except json.decoder.JSONDecodeError as e:
            print(e, data)
            breakpoint()

        return_set = {}
        if data['request'] == 'create_player':
            ## {'request': 'create_player', 'player': '<username>'}
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
                self.player2.parse_moveset(data['moveset'])
            else:
                print("This person isn't a player")

            return None

        # todo send some select player data
        # maybe limit the user's first move to select player and I will start the game?

        # overwrite a current player
        elif data['request'] == 'overwrite_player':
            #pass the old controller to the new player; just needs to exist bot side
            if self.player1 and self.player1.name == data['old_player']:
                self.player1 = new_controller
                response = {'response': 'Reassigned player 1'}
            elif self.player2 and self.player2.name == data['old_player']:
                self.player2 = new_controller
                response = {'response': 'Reassigned player 2'}
            else:
                response = {'response': "No players created or none with that name"}

            return response

        # Again the server doesn't need to know this
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

    # TODO: Close everything neatly
    def disconnect_controller(self, name=None):
        if not name:
            try:
                self.player1.shutdown()
                self.player2.shutdown()
            except AttributeError:
                raise
        else:
            if name == 'player1':
                self.player1.shutdown()
            else:
                self.player2.shutdown()
        return

    def getgamefocus(self, name):
        focus.focus_window(name)
        return

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
