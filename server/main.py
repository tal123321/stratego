import http.server
import socketserver
import random
from Board import Board
from game import game
import string
PORT = 8000

playersWaiting = []
startGame = False
counterPlayers = 1
games = {}
randomId = ""
class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global playersWaiting,counterPlayers,startGame,games,randomId
        response = ""
        params = self.parse_QS()  # Parse query parameters
        action = params.get("action")
        value = params.get("value")
        player_id = params.get("clientId")
        gameId = params.get("game_Id")
        print(gameId)
        if action == "playTurn":
            games[gameId].playTurn(value)

        if action == "signIn":
            response = "welcome" + value

        elif action == "lookingForGame":
            if player_id in playersWaiting and startGame:
                response = randomId
                startGame = False

                playersWaiting.remove(games[randomId].getPlayerUp())
                playersWaiting.remove(games[randomId].getPlayerDown())

            elif player_id not in playersWaiting:
                playersWaiting.append(player_id)
            if len(playersWaiting) >= 2 and not startGame:
                randomId = self.RandomId()
                games[randomId] = game(player_id,playersWaiting[0],True)
                response = randomId
                startGame = True

        elif action == "getPlayerId":
            response = counterPlayers
            counterPlayers+= 1

        elif action == "getBoard":
            response = games[gameId].getBoardAsString(player_id)

        elif action == "isMyTurn":
            response = str(games[gameId].turn == player_id)

        elif action == "switchCards":
            games[gameId].switchCards(value,player_id)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(bytes(f"{response}", "utf-8"))

    def parse_QS(self):
        """Parses the query string from the request URL."""
        qs = {}
        if "?" in self.path:
            qs = dict(qc.split("=") for qc in self.path.split("?")[1].split("&"))
        return qs

    def RandomId(self):
        return ''.join([random.choice(string.ascii_letters+ string.digits) for n in range(16)])


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
