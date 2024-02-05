from Board import Board
firstBoard = Board()
secondBoard = Board()
value= "6958"

firstBoard.changeBoard(int(value[0]), int(value[1]), "green")
firstBoard.changeBoard(int(value[2]), int(value[3]), "piece")
print(firstBoard.getPiece(int(value[0]),int(value[1])))
print(firstBoard.getPiece(int(value[2]),int(value[3])))