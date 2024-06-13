from Board import Board
import threading
import time
import sqlite3


class game():
    def __init__(self, playerDown, playerUp):
        self.playerDown = playerDown
        self.playerUp = playerUp
        self.board = Board(playerUp, playerDown)
        self.turn = playerDown
        self.chat = ""
        self.status = "not started"
        self.bothPlayersReady = []

        # for the first player
        self.timeThread1 = showTimeThread(300, self.playerUp, self)
        self.timeThread1.start()

        # for the second player
        self.timeThread2 = showTimeThread(300, self.playerDown, self)
        self.timeThread2.start()

    def changeRating(self, username, new_rating):
        # If the new rating is negative, set it to 0
        if new_rating < 0:
            new_rating = 0

        # Connect to the SQLite database
        conn = sqlite3.connect("database")
        cursor = conn.cursor()

        # Execute the query to update the rating for the given username
        cursor.execute("UPDATE usersInfo SET rating = ? WHERE username = ?", (new_rating, username))

        # commit Close the cursor and the connection
        conn.commit()
        cursor.close()
        conn.close()

    def getRating(self, player):
        playerUpRating = str(self.getPlayerRating(self.playerUp))
        playerDownRating = str(self.getPlayerRating(self.playerDown))
        if player == self.playerUp:
            return self.playerDown + "(" + playerDownRating + ") " + self.playerUp + "(" + playerUpRating + ")"
        else:
            return self.playerUp + "(" + playerUpRating + ") " + self.playerDown + "(" + playerDownRating + ")"

    def getPlayerRating(self, username):
        # Connect to the SQLite database
        conn = sqlite3.connect("database")
        cursor = conn.cursor()

        # Execute the query to get the rating for the given username
        cursor.execute("SELECT rating FROM usersInfo WHERE username = ?", (username,))

        # Fetch the result and return
        result = cursor.fetchone()

        # Close the cursor and the connection
        cursor.close()
        conn.close()

        return result[0]

    def getPlayerDown(self):
        return self.playerDown

    def getPlayerUp(self):
        return self.playerUp

    def getTime(self, player):
        if player == self.playerUp:
            time = self.timeThread1.getTime()
            if time == "0:00" and self.status != "not started":
                self.status = self.playerDown
            return time

        time = self.timeThread2.getTime()
        if time == "0:00" and self.status != "not started":
            self.status = self.playerUp
        return time

        # check that game is not over
        return time

    def getOtherTime(self, player):
        if player == self.playerUp:
            return self.timeThread2.getTime()
        return self.timeThread1.getTime()

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

    def readyStartGame(self,player):
        if player not in self.bothPlayersReady:
            self.bothPlayersReady.append(player)
        if len(self.bothPlayersReady) == 2:
            self.timeThread1.time = 0
            self.timeThread2.time = 0

    def playTurn(self, value, player):
        row1, col1, row2, col2 = map(int, value)
        # game has not stared
        if self.status == "not started":
            if row2 < 6 or row1 < 6:
                return
            self.switchCards(row1, col1, row2, col2, player)
        else:
            # game has started
            if self.turn != player:
                return "enemy Turn"
            self.movePiece(value, player)

    def getBoardAsArray(self, player):
        # if status is not going someone won
        if self.status not in ["going", "not started"]:

            # change the rating of the players
            if player == self.playerDown:
                self.changeRating(self.board.playerDown, self.getPlayerRating(self.board.playerDown) + 10)
                self.changeRating(self.board.playerUp, self.getPlayerRating(self.board.playerUp) - 10)
            else:
                self.changeRating(self.board.playerDown, self.getPlayerRating(self.board.playerDown) - 10)
                self.changeRating(self.board.playerUp, self.getPlayerRating(self.board.playerUp) + 10)

            return self.status
        return self.board.getBoardAsArray(player)


    def movePiece(self, value, player):
        row1, col1, row2, col2 = map(int, value)
        # Update the destination board with the piece
        if str(self.turn) == str(self.board.playerDown):
            if not self.board.checkLegalMove(row1, col1, row2, col2, player):
                return
            if self.board.movePiece(row1, col1, row2, col2):
                # if game is over winner is the one who played right now
                self.status = self.turn
        else:
            if not self.board.checkLegalMove(9 - row1, col1, 9 - row2, col2, player):
                return
            if self.board.movePiece(9 - row1, col1, 9 - row2, col2):
                # if game is over winner is the one who played right now
                self.status = self.turn

        # Switch player turn
        if self.turn == self.playerDown:
            self.turn = self.playerUp
        else:
            self.turn = self.playerDown

    def resign(self, player):
        if player == self.playerUp:
            self.status = self.playerDown
        else:
            self.status = self.playerUp

    def switchCards(self, row1, col1, row2, col2, player):
        # Update the destination board with the piece
        if str(player) == str(self.board.playerDown):
            self.board.switchCards(row1, col1, row2, col2)
        else:
            self.board.switchCards(9 - row1, col1, 9 - row2, col2)

    def sendText(self, player, value):
        self.chat += player + ": " + value + "<br>"

    def getText(self):
        return self.chat

    def getTurn(self):
        return self.turn


class showTimeThread(threading.Thread):
    def __init__(self, seconds, player, game):
        threading.Thread.__init__(self)
        self.time = seconds
        self.game = game
        self.player = player

    def run(self):
        while self.time > 0:
            time.sleep(1)
            self.time -= 1
        self.game.status = "going"

        # after the game started
        self.time = 5
        while self.time > 0:
            time.sleep(1)
            if self.game.getTurn() == self.player:
                self.time -= 1

    def getTime(self):
        minutes = self.time // 60
        remaining_seconds = self.time % 60
        return f"{minutes}:{remaining_seconds:02d}"
