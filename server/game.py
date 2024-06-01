from Board import Board
import threading
import time


class game():
    def __init__(self, playerDown, playerUp):
        self.playerDown = playerDown
        self.playerUp = playerUp
        self.board = Board(playerUp, playerDown)
        self.turn = playerDown
        self.chat = ""
        self.status = "not started"

        self.timeThread = showTimeThread(10)
        self.timeThread.start()

    def getBoardAsArray(self, player):
        # if status is not going someone won
        if self.status not in ["going", "not started"]:
            return self.status
        return self.board.getBoardAsArray(player)

    def getPlayerDown(self):
        return self.playerDown

    def getPlayerUp(self):
        return self.playerUp

    def deletePlayer(self, player):
        if player == self.playerDown:
            self.playerDown = ""
        elif player == self.playerUp:
            self.playerUp = ""
        return self.playerUp == "" and self.playerDown == ""

    def setPlayerDown(self, playerDown):
        self.playerDown = playerDown

    def SetPlayerUp(self, playerUp):
        self.playerUp = playerUp

    def playTurn(self, value):
        row1, col1, row2, col2 = map(int, value)
        # Update the destination board with the piece
        if str(self.turn) == str(self.board.playerDown):
            if self.turn != self.board.getCardOwner(row1, col1):
                return
            if self.board.movePiece(row1, col1, row2, col2, self.turn):
                # if game is over winner is the one who played right now
                self.status = self.turn
        else:
            if self.turn != self.board.getCardOwner(9 - row1, col1):
                return
            if self.board.movePiece(9 - row1, col1, 9 - row2, col2, self.turn):
                # if game is over winner is the one who played right now
                self.status = self.turn

        # Switch player turn
        if self.turn == self.playerDown:
            self.turn = self.playerUp
        else:
            self.turn = self.playerDown

    def getTime(self):
        return self.timeThread.getTime()

    def switchCards(self, value, player):
        row1, col1, row2, col2 = map(int, value)

        # Update the destination board with the piece
        if str(player) == str(self.board.playerDown):
            self.board.switchCards(row1, col1, row2, col2)
        else:
            self.board.switchCards(9 - row1, col1, 9 - row2, col2)

    def sendText(self, player, value):
        self.chat += player + ": " + value + "<br>"

    def getText(self):
        return self.chat


class showTimeThread(threading.Thread):
    def __init__(self, seconds):
        threading.Thread.__init__(self)
        self.time = seconds

    def run(self):
        while self.time > 0:
            time.sleep(1)
            self.time -= 1

    def getTime(self):
        minutes = self.time // 60
        remaining_seconds = self.time % 60
        return f"{minutes}:{remaining_seconds:02d}"
