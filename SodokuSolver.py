# SodokuSolver.py
import pprint

board1 = [
         [1,8,0,0,5,3,6,0,0],
         [3,0,0,1,0,0,0,8,0],
         [6,0,7,4,2,0,0,5,0],
         [0,0,0,6,3,1,5,0,0],
         [0,0,0,8,0,9,0,0,0],
         [0,0,6,5,7,2,0,0,0],
         [0,7,0,0,6,5,8,0,9],
         [0,3,0,0,0,7,0,0,5],
         [0,0,5,3,8,0,0,1,2]
         ]

def solveBoard(board, row, column):
    if checkBoard(board):
        return board
    if board[row][column] != 0:
        try:
            solveBoard(board, row, column + 1)
        except IndexError:
            solveBoard(board, row + 1, 0)
    for i in range(1, 10):
        if valid(i, row, column, board):
            board[row][column] = i
            try:
                solveBoard(board, row, column + 1)
            except IndexError:
                solveBoard(board, row + 1, 0)
        if checkBoard(board):
            return board
        if i == 9:
            board[row][column] = 0
    return board

def checkBoard(board):
    for i in range(len(board)):
        for j in board[i]:
            if j == 0:
                return False
                break
    else:
        return True


def valid(num, row, column, board):
    subBoardX = (row//3)*3
    subBoardY = (column//3)*3
    subBoardList = []
    for i in range(subBoardX, subBoardX+3):
        for j in range(subBoardY, subBoardY+3):
            subBoardList.append(board[i][j])

    if num not in board[row]:
        if num not in [board[i][column] for i in range(0,9)]:
            if num not in subBoardList:
                return True
    return False

# pprint.pprint(solveBoard(board1, 0, 0))



