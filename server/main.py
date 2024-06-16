import http.server
import socketserver
import random
from Board import Board
from game import game
import string
import sqlite3
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
import rsa
import urllib.parse

PORT = 8000
playersWaiting = []
startGame = False
games = {}
randomId = ""
semetricKey = ""


class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global playersWaiting, startGame, games, randomId, semetricKey
        response = ""
        params = self.parse_QS()  # Parse query parameters
        action = params.get("action")
        value = urllib.parse.unquote(params.get("value"))
        player_id = params.get("clientId")
        gameId = params.get("game_Id")

        if action == "login":
            # check if the user exist
            response = str(self.check_credentials(value.split()[0], value.split()[1]))
        elif action == "checkGameExist":
            checkIfGameExist = str(value in games)
            if checkIfGameExist == "True":
                response = json.dumps([checkIfGameExist,str(games[value].status == "not started")])
            else:
                response = json.dumps([checkIfGameExist, "False"])
        elif action == "signUp":
            response = self.sign_up(value.split()[0], value.split()[1])
        elif action == "getRating":
            response = games[gameId].getRating(player_id)
        elif action == "sendText":
            games[gameId].sendText(player_id, value)
        elif action == "resign":
            games[gameId].resign(player_id)

        elif action == "sendSemetricKey":
            print(value)
            semetricKey = urllib.parse.unquote(value)
            # publicKey = self.encrypt_data("hi",urllib.parse.unquote(value))
            # print(response)

        elif action == "playTurn":
            response = games[gameId].playTurn(value,player_id)

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
            response["time1"] = games[gameId].getOtherTime(player_id)
            response["time2"] = games[gameId].getTime(player_id)
            if isinstance(response, list) and games[gameId].deletePlayer(player_id):
                # if reached here it means both player got the message and we can erase the game
                games.pop(gameId, None)
            else:
                response = json.dumps(response)

        elif action == "readyStartGame":
            games[gameId].readyStartGame(player_id)

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
        return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])

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
        cursor = conn.cursor()

        # Check if username already exists
        check_query = "SELECT COUNT(*) FROM usersInfo WHERE username = ?;"
        cursor.execute(check_query, (username,))
        result = cursor.fetchone()[0]

        if result == 1:
            conn.close()
            return "False"  # Username already exists, return False

        # Insert the user into the database and set default rating for the user
        insert_query = "INSERT INTO usersInfo (username, password, rating) VALUES (?, ?, 100);"
        cursor.execute(insert_query, (username, password))

        # Commit the changes
        conn.commit()

        # Close the connection
        conn.close()

        return "True"  # User successfully signed up, return True

    def decrypt_data(self, enc_data, key_SYMETRIC):
        # Split the received data (assuming colon separates iv and message)
        enc_iv, enc_msg = enc_data.split(":", 1)

        # Decode base64 only on the message part
        enc_msg = b64decode(enc_msg)

        # Convert key_SYMETRIC to bytes if it's a string
        if isinstance(key_SYMETRIC, str):
            key_SYMETRIC = key_SYMETRIC.encode('utf-8')

        # Decrypt the data using AES-CBC
        cipher = AES.new(key_SYMETRIC, AES.MODE_CBC, b64decode(enc_iv))
        decrypted_data = cipher.decrypt(enc_msg)

        # Remove padding from the decrypted data
        plain_txt = decrypted_data.rstrip(b'\x00').decode('utf-8')
        return plain_txt

    def encrypt_data(self, new_data, key_SYMETRIC):
        pad = lambda s: s + (16 - len(s) % 16) * bytes(chr(16 - len(s) % 16), 'utf-8')
        raw = pad(new_data.encode('utf-8'))

        key_SYMETRIC = b64decode(key_SYMETRIC)  # Decode the base64 key
        cipher = AES.new(key_SYMETRIC, AES.MODE_CBC)
        cipher_bytes = cipher.encrypt(raw)
        iv = b64encode(cipher.iv).decode('utf-8')
        ct = b64encode(cipher_bytes).decode('utf-8')
        iv_ct = iv + ct
        return iv_ct


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
