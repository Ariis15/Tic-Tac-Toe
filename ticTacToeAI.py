import random
board = [" "]*9
helpboard = list(map(lambda x:str(x),range(9)))

def printBoard(list):
    print("-"*15)
    print("|",list[0],"|",list[1],"|",list[2], "|")
    print("-"*15)
    print("|",list[3],"|",list[4],"|",list[5], "|")
    print("-"*15)
    print("|",list[6],"|",list[7],"|",list[8], "|")
        

def placeMove(pos,tile,board):
    board[pos] = tile 
    return board

def winnerHorCell(board,cell):
    res = False
    for i in range(0,9,3):
        res = res or (board[i] == board[i+1] and board[i+1] == board[i+2] and board[i] == cell)
    return res
def winnerHor(board):
    return winnerHorCell(board,"X") or winnerHorCell(board,"O")

def winnerVerCell(board,cell):
    res = False
    for i in range(0,3):
        res = res or (board[i] == board[i+3] and board[i+3] == board[i+6] and board[i] == cell)
    return res 

def winnerVer(board):
    return winnerVerCell(board,"X") or winnerVerCell(board,"O")

def winnerDiagCell(board,cell):
    a = board[0] == board[4] and board[4] == board[8] and board[0] == cell
    b = board[2] == board[4] and board[4] == board[6] and board[2] == cell
    return a or b
def winnerDiag(board):
    return winnerDiagCell(board,"X") and winnerDiagCell(board,"O")

def xIsWinner(board):
    return winnerHorCell(board,"X") or winnerVerCell(board,"X") or winnerDiagCell(board, "X")

def oIsWinner(board):
    return winnerHorCell(board,"O") or winnerVerCell(board,"O") or winnerDiagCell(board, "O")

def freecells(board):
    list = []   
    for indx,i in enumerate(board):
        if i == " ":
            list.append(indx)
    return list


def gameOver(board):
    return xIsWinner(board) or oIsWinner(board) or freecells(board) == []

def gameLoop(move_getter):
    print(helpboard)
    board = [" "]*9
    while not gameOver(board):
        printBoard(board)
        pos = int(input("Press a number for next move: "))
        board = placeMove(pos,"X",board)
        
        if gameOver(board):
            break
        
        pos = move_getter(board)
        board = placeMove(pos,"O",board)
    printBoard(board)

def getRandomAIMove(board):
    possible_moves = freecells(board)
    return random.choice(possible_moves)
    

def boardValue(board):
    if xIsWinner(board):
        value = 100
    elif oIsWinner(board):
        value = -100
    else:
        value = 0
    
    return value

def boardValueForPiece(board,cell):
    values = [3,2,3,2,5,2,3,2,3]
    s = 0
    for i in range(9):
        if board[i] == cell:
            s += values[i]
    return s

def heuValue(board):
    if gameOver(board):
        return boardValue(board)
    
    return boardValueForPiece(board,"X") - boardValueForPiece(board, "O")

def findTheMoveFromBoards(oldboard,newboard):
    for i in range(9):
        if not oldboard[i] == newboard[i]:
            return i
        
def findChildren(board,cell):
    posPos = freecells(board)
    children = []
    for i in posPos:
        tmpBoard = board.copy()
        tmpBoard = placeMove(i,cell,tmpBoard)
        children.append(tmpBoard.copy())
    return children

def minimax(board,depth,maxPlayer):
    bestValue = 0
    bestBoard = None
    
    if depth == 0 or gameOver(board):
        return (heuValue(board),board)
    
    if maxPlayer:
        bestValue = -10000
        children = findChildren(board,"X")
        bestBoard = children[0].copy()
        for child in children:
            (val, _) = minimax(child,depth-1,False)
            bestValue = max(bestValue,val)
            
            if bestValue == val:
                bestBoard = child.copy()
                
    else:
        bestValue = 10000
        children = findChildren(board,"O")
        bestBoard = children[0].copy()
        for child in children:
            (val, _) = minimax(child,depth-1,True)
            bestValue = min(bestValue,val)
            
            if bestValue ==val:
                bestBoard = child.copy()
                
    return (bestValue,bestBoard)

def getAIMoive(board):
    data = minimax(board,4,False)
    return findTheMoveFromBoards(board,data[1])


if __name__ == "__main__":
    print(__name__) 
    gameLoop(getAIMoive)
    
