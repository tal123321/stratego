from Board import Board
class game():
    def __init__(self, playerDown,playerUp,gameStatus):
        self.playerDown = playerDown
        self.playerUp = playerUp
        self.gameStatus = gameStatus
        self.board = Board(playerUp,playerDown)
        self.turn = playerDown

    def getBoardAsString(self,player):
        return self.board.get_board_as_string(player)

    def getPlayerDown(self):
        return self.playerDown
    def getPlayerUp(self):
        return self.playerUp

    def setPlayerDown(self,playerDown):
        self.playerDown = playerDown
    def SetPlayerUp(self,playerUp):
        self.playerUp = playerUp

    def GetStatus(self):
        return self.gameStatus

    def playTurn(self,value):
        row1, col1, row2, col2 = map(int, value)

        # Update the destination board with the piece
        if str(self.turn) == str(self.board.playerDown):
            self.board.movePiece(row1, col1, row2, col2)
        else:
            self.board.movePiece(9 - row1, col1, 9 - row2, col2)

        # Switch player turn
        if self.turn == self.playerDown:
            self.turn = self.playerUp
        else:
            self.turn = self.playerDown


    def switchCards(self,value,player):
        row1, col1, row2, col2 = map(int, value)

        # Update the destination board with the piece
        if str(player) == str(self.board.playerDown):
            self.board.switchCards(row1, col1, row2, col2)
        else:
            self.board.switchCards(9 - row1, col1, 9 - row2, col2)