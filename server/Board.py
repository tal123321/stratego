import threading
import time
import sqlite3

class card:
    def __init__(self, kind, player=0, show=False):
        # show is true or false so when a card beats another it should be seen by both players
        self.kind = kind
        self.player = player
        self.show = show

    def getPlayer(self):
        return self.player

    def getShow(self):
        return self.show

    def setShow(self, show):
        self.show = show

    def getKind(self):
        return self.kind

    def setKind(self, kind):
        self.kind = kind

    def setPlayer(self, player):
        self.player = player

    def copy(self, other):
        self.kind = other.kind
        self.player = other.player
        self.show = other.show

    def shouldShow(self, player):
        return str(self.player) == str(player) or str(self.player) == "0" or self.show


class Board:
    def __init__(self, playerUp, playerDown, rows=10, columns=10):
        self.board = []
        self.playerUp = playerUp  # Assign playerUp
        self.playerDown = playerDown  # Assign playerDown
        for row in range(rows):
            current_row = []
            for col in range(columns):
                cell_content = self.determineCellContent(row, col)
                if row < 4:
                    current_row.append(card(cell_content, playerUp))
                elif row > 5:
                    current_row.append(card(cell_content, playerDown))
                else:
                    current_row.append(card(cell_content))
            self.board.append(current_row)

    def getTopPlayer(self):
        return self.playerUp

    def getbuttomPlayer(self):
        return self.playerDown

    def getBoard(self):
        return self.board

    def getPiece(self, row, col):
        return self.board[int(row)][int(col)].getKind()

    def movePiece(self, fromRow, fromCol, toRow, toCol):
        placeFrom = self.board[fromRow][fromCol]
        placeTo = self.board[toRow][toCol]

        if placeTo.getKind() == "flag":
            # game is over
            return True
        elif placeTo.getKind() == "green":
            self.board[toRow][toCol] = self.board[fromRow][fromCol]
            self.board[fromRow][fromCol] = card("green")
            return
        # there is a fight between two cards
        elif placeTo.getKind() == "bomb":
            # incase of a bomb only card 3 survives
            if placeFrom.getKind() == "image3":
                self.board[toRow][toCol] = self.board[fromRow][fromCol]
                a = self.board[toRow][toCol]
            else:
                placeTo.copy(card("green"))
        # if there is an enemy card or a one attacking a nine
        elif (placeFrom.getKind()[-1] > placeTo.getKind()[-1]) or (
                placeFrom.getKind()[-1] == "1" and placeTo.getKind()[-1] == "9"):
            self.board[toRow][toCol] = self.board[fromRow][fromCol]
        elif placeFrom.getKind()[-1] == placeTo.getKind()[-1]:
            placeTo.copy(card("green"))
        a = self.board[toRow][toCol]
        self.board[fromRow][fromCol] = card("green")
        # game is not over
        showCard = showCardThread(self.board[toRow][toCol])
        showCard.start()
        a = self.board[toRow][toCol]
        return False

    def getBoardAsArray(self, player):
        # if the player is the player and the top the board should be reversed
        reversedOrNormalBoard = self.board
        if str(player) == str(self.playerUp):
            reversedOrNormalBoard = self.board[::-1]
        boardToSend = []
        for row in reversedOrNormalBoard:
            rowArr = []
            for card in row:
                if card.shouldShow(player):
                    rowArr.append(card.getKind())
                else:
                    rowArr.append("enemy")
            boardToSend.append(rowArr)
        return boardToSend

    @staticmethod
    def determineCellContent(row, col):
        # Connect to SQLite database
        conn = sqlite3.connect("database")
        cursor = conn.cursor()

        query = f"SELECT col{col} FROM basicBoard LIMIT 1 OFFSET ?"
        # Execute the query with the given row (adjust for zero-based index)
        cursor.execute(query, (row,))

        # Fetch the result
        result = cursor.fetchone()

        # Close the connection
        conn.close()

        # Return the result
        return result[0]

    def switchCards(self, fromRow, fromCol, toRow, toCol):
        tempCard = card(self.board[toRow][toCol].getKind(), self.board[toRow][toCol].getPlayer())
        self.board[toRow][toCol].copy(self.board[fromRow][fromCol])
        self.board[fromRow][fromCol].copy(tempCard)

    def getCardOwner(self,row,col):
        return self.board[row][col].getPlayer()

    def checkLegalMove(self, row1, col1, row2, col2,player):
        card = self.board[row1][col1]
        if card.getPlayer() != player or "image" not in card.getKind() or self.board[row2][col2].getKind() == "blue":
            return False

        # Calculate the absolute difference between rows and columns
        row_diff = abs(row2 - row1)
        col_diff = abs(col2 - col1)

        # If the difference in rows or columns is more than 1
        if row_diff > 1 or col_diff > 1:
            # If the card is not a 2, return False
            if "2" not in card.getKind():
                return False
            else:
                # If the card is a 2, it can jump more than one tile
                # Check if it's a valid jump (only vertical or horizontal)
                if row_diff > 0 and col_diff > 0:
                    return False  # Diagonal jump is not allowed

                # Check if there are cards between initial and final positions
                if row_diff == 0:  # Horizontal jump
                    start_col = min(col1, col2)
                    end_col = max(col1, col2)
                    for col in range(start_col + 1, end_col):
                        if "green" not in  self.board[row1][col1].getKind():
                            return False  # Invalid jump over non-green or non-blue cards
                elif col_diff == 0:  # Vertical jump
                    start_row = min(row1, row2)
                    end_row = max(row1, row2)
                    for row in range(start_row + 1, end_row):
                        if "green" not in self.board[row][col1].getKind():
                            return False  # Invalid jump over non-green or non-blue cards
        return True


class showCardThread(threading.Thread):
    def __init__(self, card):
        threading.Thread.__init__(self)
        self.card = card

    def run(self):
        # make the card visible to both players so both player will now what card was that.
        player = self.card.setShow(True)
        time.sleep(3)
        player = self.card.setShow(False)

