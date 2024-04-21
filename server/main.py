import http.server
import socketserver
import random
from Board import Board

PORT = 8000

myArr = [1, 2]
whoseTurn = 1

board = Board(1,2)

playersWaiting = []
startGame = False
counterPlayers = 1
class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global whoseTurn,myArr,board,playersWaiting,counterPlayers,startGame
        response = ""
        params = self.parse_QS()  # Parse query parameters
        action = params.get("action")
        value = params.get("value")
        player_id = params.get("clientId")

        if action == "playTurn":
            row1, col1, row2, col2 = map(int, value)

            # Update the destination board with the piece
            if str(player_id) == str(board.playerDown):
                board.movePiece(row1,col1,row2,col2)
            else:
                board.movePiece(9-row1, col1,9-row2, col2)

            # Switch player turn
            if whoseTurn == board.getTopPlayer():
                whoseTurn = board.getbuttomPlayer()
            else:
                whoseTurn = board.getTopPlayer()

        elif action == "lookingForGame":
            if player_id not in playersWaiting:
                playersWaiting.append(player_id)
            if len(playersWaiting) >= 2 or startGame:
                if not startGame:
                    board = Board(player_id, playersWaiting[0])

                countPlayersWaiting = []
                startGame = True
                response = "True"
        elif action == "getPlayerId":
            response = counterPlayers
            counterPlayers+= 1
        elif action == "getBoard":
            print("player_id" + player_id)
            response = board.get_board_as_string(player_id)
            print(response)

        elif action == "isMyTurn":
            if str(player_id) == str(whoseTurn):
                response = "True"
            else:
                response = "False"

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


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
