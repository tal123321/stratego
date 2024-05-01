class card:
    def __init__(self,kind,player = 0):
        self.kind = kind
        self.player = player
    def getPlayer (self):
        return self.player
    def getKind (self):
        return self.kind
    def changeKind(self,kind):
        self.kind = kind
    def changePlayer(self,player):
        self.player = player

    def copy(self,other):
        self.kind = other.kind
        self.player = other.player

    def doesBelongToPlayer(self,player):
        return str(self.player) == str(player) or str(self.getPlayer()) == "0"


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

    def getPiece(self,row,col):
        return self.board[int(row)][int(col)].getKind()

    def movePiece(self,fromRow,fromCol,toRow,toCol):
        placeFrom = self.board[fromRow][fromCol]
        placeTo = self.board[toRow][toCol]

        if placeTo.getKind() == "green":
            placeTo.copy(placeFrom)
            placeFrom.copy(card("green"))
            return
        #there is a war between two cards
        if placeTo.getKind() == "bomb":
            #incase of a bomb only card 3 survives
            if placeFrom.getKind() == "image3":
                placeTo.copy(placeFrom)
            else:
                placeTo.copy(card("green"))
            placeFrom.copy(card("green"))
            return

        #if there is an enemy card
        if placeFrom.getKind()[-1] > placeTo.getKind()[-1]:
            placeTo.copy(placeFrom)
        elif self.board[toRow][toCol].getKind()[-1] == self.board[toRow][toCol].getKind()[-1]:
            placeTo.copy(card("green"))
        placeFrom.copy(card("green"))


    def get_board_as_string(self,player):
        #if the player is the player and the top the board should be reversed
        reversedOrNormalBoard = self.board
        if str(player) == str(self.playerUp):
            reversedOrNormalBoard = self.board[::-1]
        board_string = ""
        for row in reversedOrNormalBoard:
            row_string = ""
            for card in row:
                if card.doesBelongToPlayer(player):
                    row_string += card.getKind() + ' '
                else:
                    row_string+= "enemy" + ' '
            board_string += row_string.strip() + ' '
        return board_string.strip()

    @staticmethod
    def determine_cell_content(row, col):
        if (row == 7 and col == 1) or (row == 4 and col ==1):
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
        elif (row == 10 and col in [2, 3]) or (row == 1 and col in[2,3]):
            return "image9"
        elif (row == 10 and col < 10) or (row == 1 and col < 10):
            return "bomb"
        elif (row == 10 or row == 1):
            return "flag"
        elif row in [5, 6] and col in [3, 4, 7, 8]:
            return "blue"
        return "green"

    def switchCards(self,fromRow,fromCol,toRow,toCol):
        tempCard = card(self.board[toRow][toCol].getKind(),self.board[toRow][toCol].getPlayer())
        self.board[toRow][toCol].copy(self.board[fromRow][fromCol])
        self.board[fromRow][fromCol].copy(tempCard)