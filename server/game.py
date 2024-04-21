class game():
    def __init__(self,board):
        self.board = board
        self.myArr = [1, 2]
        self.whoseTurn = 1

    def playTurn(clientId,value):
        player_id = params.get("clientId")
        row1, col1, row2, col2 = map(int, value)

        # Update the destination board with the piece
        if str(player_id) == str(board.playerDown):
            board.movePiece(row1, col1, row2, col2)
        else:
            board.movePiece(9 - row1, col1, 9 - row2, col2)
        # Switch player turn
        whoseTurn = 3 - int(player_id)

    def getPlayerId(self):
        response = random.choice(myArr)
        myArr.remove(int(response))
        if len(myArr) == 0:
            myArr = [1, 2]


    