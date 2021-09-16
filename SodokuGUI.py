import pygame
import sys
import SodokuSolver


class Square(object):
    def __init__(self, num, pos, empty):
        self.num = num
        self.border = (0, 0, 0)
        self.pos = pos
        self.size = 1
        self.rect = pygame.Rect((self.pos[0] * 100, self.pos[1] * 100), (100, 100))
        self.empty = empty

    def __str__(self):
        return self.pos


class Sodoku(object):
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self, board):
        self.winWidth = 900
        self.winHeight = 900
        self.winSpacing = 100
        self.win = pygame.display.set_mode((self.winWidth, self.winHeight))
        self.board = board

        self.clock = pygame.time.Clock()
        self.squares = []
        for i in range(len(self.board)):
            self.squares.append([])
            for j in range(len(self.board)):
                if self.board[i][j] == 0:
                    self.squares[i].append(Square(self.board[i][j], (j, i), True))
                else:
                    self.squares[i].append(Square(self.board[i][j], (j, i), False))
        self.selectedSquare = None
        self.completeBoard = SodokuSolver.solveBoard(self.board, 0, 0)

        self.run()

    def drawBoard(self):
        numFont = pygame.font.SysFont('Adobe Garamond Pro', 170)
        self.win.fill(self.WHITE)
        for list in self.squares:
            for square in list:
                pygame.draw.rect(self.win,
                                 square.border,
                                 (square.pos[0] * self.winSpacing,
                                  square.pos[1] * self.winSpacing,
                                  self.winSpacing,
                                  self.winSpacing), square.size)
                if square.num != 0:
                    label = numFont.render(str(square.num), 1, self.BLACK)
                    self.win.blit(label, (square.pos[0] * self.winSpacing + 20, square.pos[1] * self.winSpacing))
        for i in range(0, self.winWidth, int(self.winWidth / 3)):
            pygame.draw.line(self.win, self.BLACK, (0, i), (self.winWidth, i), 4)
            pygame.draw.line(self.win, self.BLACK, (i, 0), (i, self.winWidth), 4)
        pygame.display.update()

    def solveBoard(self, row, column):
        if self.checkSquares():
            return self.squares
        if self.squares[row][column].num != 0:
            try:
                self.solveBoard(row, column + 1)
            except IndexError:
                self.solveBoard(row + 1, 0)
        for i in range(1, 10):
            if self.valid(i, row, column):
                self.squares[row][column].num = i
                self.squares[row][column].border = self.GREEN
                self.squares[row][column].size = 5
                self.drawBoard()

                # adjust speed here
                # pygame.time.delay(100)

                try:
                    self.solveBoard(row, column + 1)
                except IndexError:
                    self.solveBoard(row + 1, 0)
            if self.checkSquares():
                return self.board
            if i == 9:
                self.squares[row][column].num = 0
                self.squares[row][column].border = self.RED
                self.drawBoard()
                pygame.time.delay(40)

        return self.board

    def checkSquares(self):
        for i in range(len(self.squares)):
            for j in self.squares[i]:
                if j.num == 0:
                    return False
        else:
            return True

    def valid(self, num, row, column):
        subBoardX = (row // 3) * 3
        subBoardY = (column // 3) * 3
        subBoardList = []
        for i in range(subBoardX, subBoardX + 3):
            for j in range(subBoardY, subBoardY + 3):
                subBoardList.append(self.squares[i][j].num)

        if num not in [self.squares[row][i].num for i in range(0, 9)]:
            if num not in [self.squares[i][column].num for i in range(0, 9)]:
                if num not in subBoardList:
                    return True
        return False

    def checkTrue(self):
        selectedPos = self.selectedSquare.pos
        if self.selectedSquare.num == self.completeBoard[selectedPos[0]][selectedPos[1]]:
            self.selectedSquare.empty = False
            self.selectedSquare.size = 1
            self.selectedSquare.border = self.BLACK
        else:
            self.selectedSquare.num = 0
            self.selectedSquare.empty = False
            self.selectedSquare.size = 1
            self.selectedSquare.border = self.BLACK
        self.selectedSquare = None


    def run(self):
        pygame.init()
        pygame.display.set_caption('Sodoku')
        run = True
        while run:
            self.clock.tick(30)

            ev = pygame.event.get()

            for event in ev:
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for list in self.squares:
                        for square in list:
                            if square.rect.collidepoint(pos) and square.empty == True:
                                self.selectedSquare = square
                                square.border, square.size = self.RED, 3

            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                self.solveBoard(0, 0)
            if self.selectedSquare:
                if keys[pygame.K_1]:
                    self.selectedSquare.num = 1
                if keys[pygame.K_2]:
                    self.selectedSquare.num = 2
                if keys[pygame.K_3]:
                    self.selectedSquare.num = 3
                if keys[pygame.K_4]:
                    self.selectedSquare.num = 4
                if keys[pygame.K_5]:
                    self.selectedSquare.num = 5
                if keys[pygame.K_6]:
                    self.selectedSquare.num = 6
                if keys[pygame.K_7]:
                    self.selectedSquare.num = 7
                if keys[pygame.K_8]:
                    self.selectedSquare.num = 8
                if keys[pygame.K_9]:
                    self.selectedSquare.num = 9
                if keys[pygame.K_RETURN]:
                    self.checkTrue()

            self.drawBoard()

        pygame.quit()


if __name__ == '__main__':
    game = Sodoku(SodokuSolver.board1)
