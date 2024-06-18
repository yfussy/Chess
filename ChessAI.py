import random

pieceScore = {"K": 0, "Q": 900, "R": 500, "B": 330, "N": 320, "p": 100}

whiteKnightScore = [[-30, -20, -10, -10, -10, -10, -20, -30],
                    [-20, -20, 0, 0, 0, 0, -20, -20],
                    [-10, 0, 10, 15, 15, 10, 0, -10],
                    [-10, 5, 15, 20, 20, 15, 0, -10],
                    [-10, 0, 15, 20, 20, 15, 0, -10],
                    [-10, 5, 10, 15, 15, 10, 5, -10],
                    [-20, -10, 0, 5, 5, 0, -10, -20],
                    [-30, -20, -10, -10, -10, -10, -20, -30]]

blackKnightScore = [[-30, -20, -10, -10, -10, -10, -20, -30],
                    [-20, -10, 0, 5, 5, 0, -10, -20],
                    [-10, 5, 10, 15, 15, 10, 5, -10],
                    [-10, 0, 15, 20, 20, 15, 0, -10],
                    [-10, 5, 15, 20, 20, 15, 0, -10],
                    [-10, 0, 10, 15, 15, 10, 0, -10],
                    [-20, -20, 0, 0, 0, 0, -20, -20],
                    [-30, -20, -10, -10, -10, -10, -20, -30]]

whiteQueenScore = [[-20, -10, -10, -5, -5, -10, -10, -20],
                   [-10, 0, 0, 0, 0, 0, 0, -10],
                   [-10, 0, 5, 5, 5, 5, 0, -10],
                   [-5, 0, 5, 5, 5, 5, 0, -5],
                   [-5, 0, 5, 5, 5, 5, 0, 0],
                   [-10, 0, 5, 5, 5, 5, 5, -10],
                   [-10, 0, 0, 0, 0, 5, 0, -10],
                   [-20, -10, -10, -5, -5, -10, -10, -20]]

blackQueenScore = [[-20, -10, -10, -5, -5, -10, -10, -20],
                   [-10, 0, 5, 0, 0, 0, 0, -10],
                   [-10, 5, 5, 5, 5, 5, 0, -10],
                   [0, 0, 5, 5, 5, 5, 0, -5],
                   [-5, 0, 5, 5, 5, 5, 0, -5],
                   [-10, 0, 5, 5, 5, 5, 0, -10],
                   [-10, 0, 0, 0, 0, 0, 0, -10],
                   [-20, -10, -10, -5, -5, -10, -10, -20]]

whiteRookScore = [[0, 0, 0, 0, 0, 0, 0, 0],
                  [5, 10, 10, 10, 10, 10, 10, 5],
                  [-5, 0, 0, 0, 0, 0, 0, -5],
                  [-5, 0, 0, 0, 0, 0, 0, -5],
                  [-5, 0, 0, 0, 0, 0, 0, -5],
                  [-5, 0, 0, 0, 0, 0, 0, -5],
                  [-5, 0, 0, 0, 0, 0, 0, -5],
                  [0, 0, 0, 5, 5, 0, 0, 0], ]

blackRookScore = [[0, 0, 0, 5, 5, 0, 0, 0],
                  [-5, 0, 0, 0, 0, 0, 0, -5],
                  [-5, 0, 0, 0, 0, 0, 0, -5],
                  [-5, 0, 0, 0, 0, 0, 0, -5],
                  [-5, 0, 0, 0, 0, 0, 0, -5],
                  [-5, 0, 0, 0, 0, 0, 0, -5],
                  [5, 10, 10, 10, 10, 10, 10, 5],
                  [0, 0, 0, 0, 0, 0, 0, 0]]
whiteBishopScore = [[-20, -10, -10, -10, -10, -10, -10, -20],
                    [-10, 0, 0, 0, 0, 0, 0, -10],
                    [-10, 0, 5, 10, 10, 5, 0, -10],
                    [-10, 5, 5, 10, 10, 5, 5, -10],
                    [-10, 0, 10, 10, 10, 10, 0, -10],
                    [-10, 10, 10, 10, 10, 10, 10, -10],
                    [-10, 5, 0, 0, 0, 0, 5, -10],
                    [-20, -10, -10, -10, -10, -10, -10, -20]]

blackBishopScore = [[-20, -10, -10, -10, -10, -10, -10, -20],
                    [-10, 5, 0, 0, 0, 0, 5, -10],
                    [-10, 10, 10, 10, 10, 10, 10, -10],
                    [-10, 0, 10, 10, 10, 10, 0, -10],
                    [-10, 5, 5, 10, 10, 5, 5, -10],
                    [-10, 0, 5, 10, 10, 5, 0, -10],
                    [-10, 0, 0, 0, 0, 0, 0, -10],
                    [-20, -10, -10, -10, -10, -10, -10, -20]]

whitePawnScore = [[50, 50, 50, 50, 50, 50, 50, 50],
                  [50, 50, 50, 50, 50, 50, 50, 50],
                  [10, 10, 20, 30, 30, 20, 10, 10],
                  [5, 5, 10, 25, 25, 10, 5, 5],
                  [0, 0, 0, 20, 20, 0, 0, 0],
                  [5, -5, -10, 0, 0, -10, -5, 5],
                  [5, 10, 10, -20, -20, 10, 10, 5],
                  [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScore = [[0, 0, 0, 0, 0, 0, 0, 0],
                  [5, 10, 10, -20, -20, 10, 10, 5],
                  [5, -5, -10, 0, 0, -10, -5, 5],
                  [0, 0, 0, 20, 20, 0, 0, 0],
                  [5, 5, 10, 25, 25, 10, 5, 5],
                  [10, 10, 20, 30, 30, 20, 10, 10],
                  [50, 50, 50, 50, 50, 50, 50, 50],
                  [50, 50, 50, 50, 50, 50, 50, 50]]

piecePositionScores = {"bp": blackPawnScore, "wp": whitePawnScore, "wN": whiteKnightScore, "bN": blackKnightScore,
                       "wQ": whiteQueenScore, "bQ": blackQueenScore, "wB": whiteBishopScore, "bB": blackBishopScore,
                       "wR": whiteRookScore, "bR": blackRookScore}

CHECKMATE = 10000000
STALEMATE = 0
DEPTH = 1


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findBestMove(gs, validMoves):
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    # findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    print(counter)
    return nextMove


def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore

    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore


def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter

    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move, score)
        gs.undoMove()
        # pruning
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                # positionally scored
                piecePositionScore = 0
                if square[1] != 'K':
                    piecePositionScore = piecePositionScores[square][row][col]

                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePositionScore
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + piecePositionScore

    return score


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]

    return score
