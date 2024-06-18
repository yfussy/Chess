class GameState:

    def __init__(self):

        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False
        self.enPassantPossible = ()  # cords for the square where en-passant is available
        self.enPassantPossibleLog = [self.enPassantPossible]
        self.whiteCastleKingSide = True
        self.whiteCastleQueenSide = True
        self.blackCastleKingSide = True
        self.blackCastleQueenSide = True
        self.castleRightsLog = [CastleRights(self.whiteCastleKingSide, self.blackCastleKingSide,
                                             self.whiteCastleQueenSide, self.blackCastleQueenSide)]

    def moveFunctions(self, piece):
        moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                         'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        return moveFunctions[piece]

    def makeMove(self, move):
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.board[move.startRow][move.startCol] = "--"
        self.moveLog.append(move)  # log the move
        self.whiteToMove = not self.whiteToMove  # swap player
        if move.pieceMoved == "wK":  # update king's location
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        # update enpassantPossible variable
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enPassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enPassantPossible = ()

        # pawn promotion
        if move.isPawnPromotion:
            # promotedPiece = input("Promote to Q, R, B, or N:")
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # en-passant
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"

        self.enPassantPossibleLog.append(self.enPassantPossible)

        # castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  # king side castle
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = "--"
            else:  # queen side castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = "--"

        # update castling rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.whiteCastleKingSide, self.blackCastleKingSide,
                                                 self.whiteCastleQueenSide, self.blackCastleQueenSide))


    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":  # update king's location
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            # en-passant undo
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured

            self.enPassantPossibleLog.pop()
            self.enPassantPossible = self.enPassantPossibleLog[-1]

            # undo castling rights
            self.castleRightsLog.pop()
            castleRights = self.castleRightsLog[-1]
            self.whiteCastleKingSide = castleRights.wks
            self.blackCastleKingSide = castleRights.bks
            self.whiteCastleQueenSide = castleRights.wqs
            self.blackCastleQueenSide = castleRights.bqs

            # undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:  # king side
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = "--"
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = "--"

            self.checkmate = False
            self.stalemate = False

    def updateCastleRights(self, move):
        if move.pieceMoved == "wK":
            self.whiteCastleKingSide = False
            self.whiteCastleQueenSide = False
        elif move.pieceMoved == "bK":
            self.blackCastleKingSide = False
            self.blackCastleQueenSide = False
        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0:
                    self.whiteCastleQueenSide = False
                elif move.startCol == 7:
                    self.whiteCastleKingSide = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0:
                    self.blackCastleQueenSide = False
                elif move.startCol == 7:
                    self.blackCastleKingSide = False

    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:

            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break

                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()

        if len(moves) == 0:
            if self.inCheck:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        return moves

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        move = Move
        move.inCheck = False

        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        types = endPiece[1]
                        if (0 <= j <= 3 and types == 'R') or \
                                (4 <= j <= 7 and types == 'B') or \
                                (i == 1 and types == 'p' and (
                                        (enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                (types == 'Q') or (i == 1 and types == 'K'):
                            if possiblePin == ():
                                inCheck = True
                                move.inCheck = True
                                checks.append((endRow, endCol, d[0], d[1],))
                                break
                            else:
                                pins.append(possiblePin)
                        else:
                            break
                else:
                    break

        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    move.inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions(piece)(r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            backRow = 0
            enemyColor = 'b'
            kingRow, kingCol = self.whiteKingLocation
        else:
            moveAmount = 1
            startRow = 1
            backRow = 7
            enemyColor = 'w'
            kingRow, kingCol = self.blackKingLocation
        pawnPromotion = False

        if self.board[r + moveAmount][c] == "--":  # normal pawn move
            if not piecePinned or pinDirection == (moveAmount, 0):
                if r + moveAmount == backRow:
                    pawnPromotion = True
                moves.append(Move((r, c), (r + moveAmount, c), self.board, isPawnPromotion=pawnPromotion))
                if r == startRow and self.board[r + 2 * moveAmount][c] == "--":
                    moves.append(Move((r, c), (r + 2 * moveAmount, c), self.board))

        if c - 1 >= 0:
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r + moveAmount][c - 1][0] == enemyColor:
                    if r + moveAmount == backRow:
                        pawnPromotion = True
                    moves.append(Move((r, c), (r + moveAmount, c - 1), self.board, isPawnPromotion=pawnPromotion))
                if (r + moveAmount, c - 1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c:
                            insideRange = range(kingCol + 1, c - 1)
                            outsideRange = range(c + 1, 8)
                        else:
                            insideRange = range(kingCol - 1, c, -1)
                            outsideRange = range(c - 2, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != "--":
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == enemyColor and (square[1] == 'R' or square[1] == 'Q'):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r, c), (r + moveAmount, c - 1), self.board, isEnpassantMove=True))

        if c + 1 <= 7:
            if not piecePinned or pinDirection == (moveAmount, 1):
                if self.board[r + moveAmount][c + 1][0] == enemyColor:
                    if r + moveAmount == backRow:
                        pawnPromotion = True
                    moves.append(Move((r, c), (r + moveAmount, c + 1), self.board, isPawnPromotion=pawnPromotion))
                if (r + moveAmount, c + 1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c:
                            insideRange = range(kingCol + 1, c)
                            outsideRange = range(c + 2, 8)
                        else:
                            insideRange = range(kingCol - 1, c + 1, -1)
                            outsideRange = range(c - 1, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != "--":
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == enemyColor and (square[1] == 'R' or square[1] == 'Q'):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r, c), (r + moveAmount, c + 1), self.board, isEnpassantMove=True))

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break

    def getKnightMoves(self, r, c, moves):
        piecePinned = False

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)
        self.getCastleMoves(r, c, moves, allyColor)

    def squareUnderAttack(self, r, c, allyColor):
        enemyColor = 'w' if allyColor == 'b' else 'b'
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:
                        break
                    if endPiece[0] == enemyColor:
                        types = endPiece[1]
                        if (0 <= j <= 3 and types == 'R') or \
                                (4 <= j <= 7 and types == 'B') or \
                                (i == 1 and types == 'p' and (
                                        (enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                (types == 'Q') or (i == 1 and types == 'K'):
                            return True
                        else:
                            break
                else:
                    break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    return True
        return False

    def getCastleMoves(self, r, c, moves, allyColor):
        inCheck = self.squareUnderAttack(r, c, allyColor)
        if inCheck:
            return
        if (self.whiteToMove and self.whiteCastleKingSide) or (not self.whiteToMove and self.blackCastleKingSide):
            self.getKingSideCastleMoves(r, c, moves, allyColor)
        if (self.whiteToMove and self.whiteCastleQueenSide) or (not self.whiteToMove and self.blackCastleQueenSide):
            self.getQueenSideCastleMoves(r, c, moves, allyColor)

    def getKingSideCastleMoves(self, r, c, moves, allyColor):
        if self.board[r][c + 1] == "--" and self.board[r][c + 2] == "--" and \
                not self.squareUnderAttack(r, c + 1, allyColor) and not self.squareUnderAttack(r, c + 2, allyColor):
            moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))

    def getQueenSideCastleMoves(self, r, c, moves, allyColor):
        if self.board[r][c - 1] == "--" and self.board[r][c - 2] == "--" and self.board[r][c - 3] == "--" and \
                not self.squareUnderAttack(r, c - 1, allyColor) and not self.squareUnderAttack(r, c - 2, allyColor):
            moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))



    # def findCheck(self):
    #     validMoves = self.getValidMoves()
    #     # checkMoveLog = Move.checkMove
    #     # for checkMove in checkMoveLog:
    #     #     for validMove in validMoves:
    #     #         check = (validMove.pieceMoved, validMove.endRow, validMove.endCol)
    #     #         if check == checkMove:
    #     #             self.makeMove(validMove)
    #     #             if self.whiteToMove:
    #     #                 if not self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1], 'w'):
    #     #                     Move.checkMove.remove(checkMove)
    #     #             else:
    #     #                 if not self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1], 'b'):
    #     #                     Move.checkMove.remove(checkMove)
    #     #             self.undoMove()
    #     for move in validMoves:
    #         check = (move.pieceMoved, move.endRow, move.endCol)
    #         self.makeMove(move)
    #         if self.whiteToMove:
    #             if self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1], 'w'):
    #                 if check not in move.checkMove:
    #                     Move.checkMove.append(check)
    #             else:
    #                 if check in move.checkMove:
    #                     Move.checkMove.remove(check)
    #         else:
    #             if self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1], 'b'):
    #                 if check not in move.checkMove:
    #                     Move.checkMove.append(check)
    #             else:
    #                 if check in move.checkMove:
    #                     Move.checkMove.remove(check)
    #         self.undoMove()


class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    checkmateMove = []
    checkMove = []
    inCheck = False

    def __init__(self, startSq, endSq, board, isEnpassantMove=False, isPawnPromotion=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isEnpassantMove = isEnpassantMove
        self.isPawnPromotion = isPawnPromotion
        self.isCastleMove = isCastleMove

        if isEnpassantMove:
            self.pieceCaptured = 'bp' if self.pieceMoved == 'wp' else 'wp'

        self.isCapture = self.pieceCaptured != "--"

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    # overriding the str() func
    def __str__(self):
        gs = GameState()

        # castle move
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"

        endSquare = self.getRankFile(self.endRow, self.endCol)

        # pawn moves
        if self.pieceMoved[1] == 'p':
            moveString = self.colsToFiles[self.startCol]
            # pawn capture
            if self.isCapture:
                moveString = moveString + 'x'
                # pawn promotion
                if self.isPawnPromotion:
                    moveString = moveString + endSquare + '=' + 'Q'
                    return moveString

            else:
                return endSquare

            return moveString + endSquare

        # other pieces
        else:
            moveString = self.pieceMoved[1]
            if self.isCapture:
                moveString += 'x'
            # if self.checkmateMove:
            #     for i in range(len(self.checkmateMove)):
            #         check = self.checkmateMove[i]
            #         if self.pieceMoved + endSquare == check[0] + self.getRankFile(check[1], check[2]):
            #             return moveString + endSquare + '#'
            # if self.checkMove:
            #     for i in range(len(self.checkMove)):
            #         check = self.checkMove[i]
            #         if self.pieceMoved + endSquare == check[0] + self.getRankFile(check[1], check[2]):
            #             return moveString + endSquare + '+'
            return moveString + endSquare
