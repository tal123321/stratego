import http.server
import socketserver
import random
from Board import Board

PORT = 8000
ImageLocation = ""

myArr = [1, 2]
whoseTurn = 1

firstBoard = Board()
secondBoard = Board()


class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global ImageLocation, whoseTurn
        response = ""
        params = self.parse_QS()  # Parse query parameters
        action = params.get("action")
        value = params.get("value")
        if action == "playTurn":
            print(value)
            piece = firstBoard.getPiece(int(value[0]), int(value[1]))

            player_id = params.get("clientId")
            if action == "playTurn":
                player_id = params.get("clientId")
                row1, col1, row2, col2 = map(int, value)

                # Get the piece from the source board
                if player_id == str(1):
                    piece = firstBoard.getPiece(row1, col1)
                else:
                    piece = secondBoard.getPiece(row1, col1)

                # Update the destination board with the piece
                if player_id == str(1):
                    firstBoard.changeBoard(row1, col1, "green")
                    firstBoard.changeBoard(row2, col2, piece)
                    secondBoard.changeBoard(9 - row1, col1, "green")
                    secondBoard.changeBoard(9 - row2, col2, "enemy")
                else:
                    secondBoard.changeBoard(row1, col1, "green")
                    secondBoard.changeBoard(row2, col2, piece)
                    firstBoard.changeBoard(9 - row1, col1, "green")
                    firstBoard.changeBoard(9 - row2, col2, "enemy")

                # Switch player turn
                whoseTurn = 3 - int(player_id)
        elif action == "getPlayerId":
            response = random.choice(myArr)
            #myArr.remove(int(response))

        elif action == "getBoard":
            player_id = params.get("clientId")
            if str(player_id) == "1":
                response = firstBoard.get_board_as_string()
            elif str(player_id) == "2":
                response = secondBoard.get_board_as_string()

        elif action == "isMyTurn":
            player_id = params.get("clientId")
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
