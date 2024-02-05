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
        global ImageLocation, whoseTurn, count
        response = ""
        params = self.parse_QS()  # Parse query parameters
        action = params.get("action")
        value = params.get("value")
        if action == "playTurn":
            print(value)
            piece = firstBoard.getPiece(int(value[0]), int(value[1]))

            playerId = params.get("clientId")
            if playerId == str(1):
                # change the first Board
                firstBoard.changeBoard(int(value[0]), int(value[1]), "green")
                firstBoard.changeBoard(int(value[2]), int(value[3]), piece)

                # change the second Board
                secondBoard.changeBoard(int(value[0]), int(value[1]), "green")
                secondBoard.changeBoard(int(value[2]), int(value[3]), piece)
            elif playerId == str(2):
                # change the first Board
                secondBoard.changeBoard(int(value[0]), int(value[1]), "green")
                secondBoard.changeBoard(int(value[2]), int(value[3]), piece)

                # change the second Board
                firstBoard.changeBoard(int(value[0]), int(value[1]), "green")
                firstBoard.changeBoard(int(value[2]), int(value[3]), piece)
            whoseTurn = 3 - int(playerId)
        elif action == "getPlayerId":
            response = random.choice(myArr)
            myArr.remove(int(response))

        elif action == "getBoard":
            playerId = params.get("clientId")
            if str(playerId) == "1":
                response = firstBoard.get_board_as_string()
            elif str(playerId) == "2":
                response = secondBoard.get_board_as_string()

        elif action == "isMyTurn":
            playerId = params.get("clientId")
            if str(playerId) == str(whoseTurn):
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
