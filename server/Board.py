import threading
import time


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

    def changeKind(self, kind):
        self.kind = kind

    def changePlayer(self, player):
        self.player = player

    def copy(self, other):
        self.kind = other.kind
        self.player = other.player

    def shouldShow(self, player):
        return str(self.player) == str(player) or str(self.getPlayer()) == "0" or self.show


class Board:
    def __init__(self, playerUp, playerDown, rows=10, columns=10):
        self.board = []
        self.playerUp = playerUp  # Assign playerUp
        self.playerDown = playerDown  # Assign playerDown
        for row in range(rows):
            current_row = []
            for col in range(columns):
                cell_content = self.determine_cell_content(row + 1, col + 1)
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

    def movePiece(self, fromRow, fromCol, toRow, toCol,player):
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
            else:
                placeTo.copy(card("green"))
            placeFrom.copy(card("green"))
        # if there is an enemy card or a one attacking a nine
        elif (placeFrom.getKind()[-1] > placeTo.getKind()[-1]) or (
                placeFrom.getKind()[-1] == "1" and placeTo.getKind()[-1] == "9"):
            self.board[toRow][toCol] = self.board[fromRow][fromCol]
        elif placeFrom.getKind()[-1] == placeTo.getKind()[-1]:
            placeTo.copy(card("green"))
        self.board[fromRow][fromCol] = card("green")
        # game is not over
        showCard = ThreadClass(self.board[toRow][toCol])
        showCard.start()
        return False

    def getBoardAsString(self, player):
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
    def determine_cell_content(row, col):
        if (row == 7 and col == 1) or (row == 4 and col == 1):
            return "image1"
        elif (row == 7 and col < 10) or (row == 4 and col < 10):
            return "image2"
        elif ((row == 7) or (row == 8 and col < 5)) or (row == 4 or (row == 3 and col < 5)):
            return "image3"
        elif (row == 8 and col < 9) or (row == 3 and col < 9):
            return "image4"
        elif (row == 8 or (row == 9 and col < 3)) or (row == 3 or (row == 2 and col < 3)):
            return "image5"
        elif (row == 9 and col < 7) or (row == 2 and col < 7):
            return "image6"
        elif (row == 9 and col < 10) or (row == 2 and col < 10):
            return "image7"
        elif (row == 9 or (row == 10 and col == 1)) or (row == 2 or (row == 1 and col == 1)):
            return "image8"
        elif (row == 10 and col in [2, 3]) or (row == 1 and col in [2, 3]):
            return "image9"
        elif (row == 10 and col < 10) or (row == 1 and col < 10):
            return "bomb"
        elif row == 10 or row == 1:
            return "flag"
        elif row in [5, 6] and col in [3, 4, 7, 8]:
            return "blue"
        return "green"

    def switchCards(self, fromRow, fromCol, toRow, toCol):
        tempCard = card(self.board[toRow][toCol].getKind(), self.board[toRow][toCol].getPlayer())
        self.board[toRow][toCol].copy(self.board[fromRow][fromCol])
        self.board[fromRow][fromCol].copy(tempCard)

    def getCardOwner(self,row,col):
        return self.board[row][col].getPlayer()


class ThreadClass(threading.Thread):
    def __init__(self, card):
        threading.Thread.__init__(self)
        self.card = card

    def run(self):
        # make the card visible to both players so both player will now what card was that.
        player = self.card.setShow(True)
        time.sleep(5)
        player = self.card.setShow(False)
