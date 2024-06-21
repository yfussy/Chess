import sys

import pygame as p
import asyncio
import ChessEngine, ChessAI
import os

BOARD_HEIGHT = BOARD_WIDTH = 512
MOVE_LOG_PANEL_WIDTH = 350
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 30
IMAGES = {}


def loadImages():
    pieces = ['bp', 'bR', 'bN', 'bB', 'bK', 'bQ', 'wp', 'wR', 'wN', 'wB', 'wK', 'wQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(os.path.dirname(os.path.realpath(__file__)) +"/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


async def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Georgia", 14, False, False)
    gs = ChessEngine.GameState()
    move = ChessEngine.Move
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    playerOne = True  # White: player -> True || Ai -> False
    playerTwo = False  # Black: player -> True || Ai -> False

    while True:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                sys.exit()
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col) or col >= 8:  # checks whether the square selected twice or not
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:  # second click = move
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                # gs.findMate()
                                # gs.findCheck()
                                moveMade = True
                                animate = True
                                sqSelected = ()  # reset user clicks
                                playerClicks = []  # reset user clicks
                        if not moveMade:
                            playerClicks = [sqSelected]
            # key handler
            elif e.type == p.KEYDOWN:
                # undo (z)
                if e.key == p.K_z:
                    if humanTurn and (not playerOne or not playerTwo):
                        gs.undoMove()
                        gs.undoMove()
                    else:
                        gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False

                # reset game (r)
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

        # AI move finder
        if not gameOver and not humanTurn:
            AIMove = ChessAI.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = ChessAI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)

        if gs.checkmate or gs.stalemate:
            gameOver = True
            drawEndGameText(screen,
                            "Stalemate" if gs.stalemate else "Black wins by checkmate" if gs.whiteToMove else "White wins by checkmate",
                            gs)

        clock.tick(MAX_FPS)
        p.display.flip()
        await asyncio.sleep(0)


def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen)  # draw square on the board
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)  # draw pieces on top of those square
    drawMoveLog(screen, gs, moveLogFont)
    drawColLabel(screen, moveLogFont)
    drawRowLabel(screen, moveLogFont)


def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value
            s.fill(p.Color('turquoise'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            for move in validMoves:
                enemyColor = 'b' if gs.whiteToMove else 'w'
                # highlight capture move
                if move.startRow == r and move.startCol == c and gs.board[move.endRow][move.endCol][
                    0] == enemyColor or move.isEnpassantMove:
                    s.fill(p.Color('red'))
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))
                # highlight move square
                if move.startRow == r and move.startCol == c and not gs.board[move.endRow][move.endCol][
                                                                         0] == enemyColor and not move.isEnpassantMove:
                    s.fill(p.Color('yellow'))
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))
    if len(gs.moveLog) != 0:
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        move = gs.moveLog[-1]
        s.fill(p.Color('green'))
        screen.blit(s, (move.startCol * SQ_SIZE, move.startRow * SQ_SIZE))
        screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawColLabel(screen, font):
    cols = ['8', '7', '6', '5', '4', '3', '2', '1']
    textColors = ['white', 'grey']
    w = 0

    for i in range(len(cols)):
        c = 1 if (i + 1) % 2 == 1 else 0
        textObject = font.render(cols[i], True, p.Color(textColors[c]))
        textLocation = (5, w)
        screen.blit(textObject, textLocation)
        w += 64

def drawRowLabel(screen ,font):
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    textColors = ['white', 'grey']
    w = 54

    for i in range(len(files)):
        c = 0 if (i + 1) % 2 == 1 else 1
        textObject = font.render(files[i], True, p.Color(textColors[c]))
        textLocation = (w, 494)
        screen.blit(textObject, textLocation)
        w += 64

def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i // 2 + 1) + ". " + str(moveLog[i]) + "   "
        if i + 1 < len(moveLog):  # black make move
            moveString += str(moveLog[i + 1]) + "   "
        moveTexts.append(moveString)

    movePerRow = 3
    padding = 10
    textY = padding
    lineSpacing = 2
    for i in range(0, len(moveTexts), movePerRow):
        text = ""
        for j in range(movePerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i + j]
        textObject = font.render(text, True, p.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing


def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 5
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)

        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)

        if move.pieceCaptured != "--":
            if move.isEnpassantMove:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSquare = p.Rect(move.endCol * SQ_SIZE, enPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)

        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(100)


def drawEndGameText(screen, text, gs):
    whiteToMove = gs.whiteToMove
    if whiteToMove:
        font = p.font.SysFont("Georgia", 32, True, False)
        textObject = font.render(text, False, p.Color('Gray'))
        textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2,
                                                                    BOARD_HEIGHT / 2 - textObject.get_height() / 2)
        screen.blit(textObject, textLocation)
        textObject = font.render(text, False, p.Color("Black"))
        screen.blit(textObject, textLocation.move(2, 2))
    else:
        font = p.font.SysFont("Georgia", 32, True, False)
        textObject = font.render(text, False, p.Color('Gray'))
        textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2,
                                                                    BOARD_HEIGHT / 2 - textObject.get_height() / 2)
        screen.blit(textObject, textLocation)
        textObject = font.render(text, False, p.Color("White"))
        screen.blit(textObject, textLocation.move(2, 2))


if __name__ == "__main__":
    asyncio.run(main())
