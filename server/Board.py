class Board:
    def __init__(self, rows=10, columns=10):
        self.board = []
        for row in range(rows):
            current_row = []
            for col in range(columns):
                cell_content = self.determine_cell_content(row+1, col+1)
                current_row.append(cell_content)
            self.board.append(current_row)

    def getBoard(self):
        return self.board

    def getPiece(self,row,col):
        return self.board[int(row)][int(col)]

    def changeBoard(self, row, col, val):
        self.board[int(row)][int(col)] = val

    def get_board_as_string(self):
        board_string = ""
        for row in self.board:
            row_string = ' '.join(map(str, row))
            board_string += row_string + ' '
        return board_string.rstrip()

    @staticmethod
    def determine_cell_content(row, col):
        if row == 7 and col == 1:
            return "image1"
        elif row == 7 and col < 10:
            return "image2"
        elif row == 7 or row == 8 and col < 5:
            return "image3"
        elif row == 8 and col < 9:
            return "image4"
        elif row == 8 or row == 9 and col < 3:
            return "image5"
        elif row == 9 and col < 7:
            return "image6"
        elif row == 9 and col < 10:
            return "image7"
        elif row == 9 or row == 10 and col == 1:
            return "image8"
        elif row == 10 and col in [2, 3]:
            return "image9"
        elif row == 10 and col < 10:
            return "bomb"
        elif row == 10:
            return "flag"
        elif row < 5:
            return "enemy"
        elif row in [5, 6] and col in [3, 4, 7, 8]:
            return "blue"
        return "green"
