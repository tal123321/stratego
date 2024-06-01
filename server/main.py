import http.server
import socketserver
import random
from Board import Board
from game import game
import string
import sqlite3
import json

PORT = 8000

playersWaiting = []
startGame = False
games = {}
randomId = ""


class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global playersWaiting, startGame, games, randomId
        response = ""
        params = self.parse_QS()  # Parse query parameters
        action = params.get("action")
        value = params.get("value")
        player_id = params.get("clientId")
        gameId = params.get("game_Id")

        if action == "login":
            # check if the user exist
            # Replace "%20" with space
            value = value.replace("%20", " ")
            response = str(self.check_credentials(value.split()[0], value.split()[1]))
        elif action == "signUp":
            # Replace "%20" with space
            value = value.replace("%20", " ")
            response = self.sign_up(value.split()[0], value.split()[1])
        elif action == "sendText":
            games[gameId].sendText(player_id, value)

        elif action == "playTurn":
            games[gameId].playTurn(value)

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
                games[randomId] = game(player_id, playersWaiting[0])
                response = randomId
                startGame = True

        elif action == "getGame":
            response = {}  # board,chat,time
            response["board"] = games[gameId].getBoardAsArray(player_id)
            response["chat"] = games[gameId].getText()
            response["time"] = games[gameId].getTime()
            if isinstance(response, list) and games[gameId].deletePlayer(player_id):
                # if reached here it means both player got the message and we can erase the game
                games.pop(gameId, None)
            else:
                response = json.dumps(response)

        elif action == "isMyTurn":
            response = str(games[gameId].turn == player_id)

        elif action == "switchCards":
            games[gameId].switchCards(value, player_id)

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
        return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])

    def check_credentials(self, username, password):
        # Connect to the database
        conn = sqlite3.connect("database")
        curr = conn.cursor()

        # create and use the query to check if user is in the database
        check_query = '''SELECT COUNT(*) FROM usersInfo WHERE username = ? AND password = ?;'''
        curr.execute(check_query, (username, password))

        # Fetch the result of the query
        result = curr.fetchone()[0]

        # Close the connection
        curr.close()
        conn.close()

        # If the result is 1, the username and password exist; otherwise, they don't
        return result == 1

    def sign_up(self, username, password):
        # Connect to the database
        conn = sqlite3.connect("database")
        curr = conn.cursor()

        # check if username already exists
        check_query = '''SELECT COUNT(*) FROM usersInfo WHERE username = ?;'''
        curr.execute(check_query, (username,))

        # Fetch the result of the query
        result = curr.fetchone()[0]
        if result == 1:
            return "False"

        # create and use the query to add the user to the database
        insert_query = '''INSERT INTO usersInfo (username, password) VALUES (?, ?);'''
        curr.execute(insert_query, (username, password))

        # Commit the changes
        conn.commit()

        # Close the connection
        curr.close()
        conn.close()

        return "True"  # if the user was added to the database


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
