import pygame
from const import *
from square import Square
from piece import *
from move import Move
import copy
from sound import Sound
import os

class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(file)]
    
        self.last_move =  None
        self.check_castle = False
        self._create()
        self._add_piece('white')
        self._add_piece('black' )
        
    def calc_moves(self, piece, row, col, bool=True):
        #calculates valid moves for each piece for each position
        diagonal = [(-1, 1), (-1, -1), (1, -1), (1, 1)]
        straight = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        def Pawn_moves():
            #steps
            steps = 1 if piece.moved else 2
            
            #vertical
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for pos_move_row in range(start, end, piece.dir):
                if Square.in_range(pos_move_row):
                    if self.squares[pos_move_row][col].isempty():
                        #initial and final move squares
                        initial = Square(row, col)
                        final = Square(pos_move_row, col)
                        #add move
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                #append move
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                    #blocked
                    else: break
                #not in range
                else: break
            #diagonal
            pos_move_row = row + piece.dir
            pos_move_cols = [col-1, col+1]
            for pos_move_col in pos_move_cols:
                if Square.in_range(pos_move_row, pos_move_col):
                    if self.squares[pos_move_row][pos_move_col].has_rival(piece.color):
                        #initial and final move squares
                        initial = Square(row, col)
                        final_piece = self.squares[pos_move_row][pos_move_col].piece
                        final = Square(pos_move_row, pos_move_col, final_piece)
                        #create move
                        move = Move(initial, final)
                        
                        #check is in check
                        if bool:
                            if not self.in_check(piece, move):
                                #append move
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
            
            #en passant
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            #left
            if Square.in_range(col-1) and row == r:
                if self.squares[row][col-1].has_rival(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            #initial and final move squares
                            initial = Square(row, col)
                            final_piece = self.squares[row][col-1].piece
                            final = Square(fr , col-1, p)
                            #create move
                            move = Move(initial, final)
                            
                            #check is in check
                            if bool:
                                if not self.in_check(piece, move):
                                    #append move
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                                
            #right
            if Square.in_range(col+1) and row == r:
                if self.squares[row][col+1].has_rival(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            #initial and final move squares
                            initial = Square(row, col)
                            final_piece = self.squares[row][col-1].piece
                            final = Square(fr , col+1, p)
                            #create move
                            move = Move(initial, final)
                            
                            #check is in check
                            if bool:
                                if not self.in_check(piece, move):
                                    #append move
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                        
        def Knight_moves():
            pos_moves = [
                (row - 2, col + 1),
                (row - 2, col - 1),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row - 1, col + 2),
                (row - 1, col - 2),
                (row + 1, col + 2),
                (row + 1, col - 2),
            ]
            
            for possible_move in pos_moves:
                possible_row, possible_col = possible_move
                if Square.in_range(possible_row, possible_col):
                    if self.squares[possible_row][possible_col].isempty_or_rival(piece.color):
                        #create squares of move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_row][possible_col].piece
                        final = Square(possible_row, possible_col, final_piece)
                        #create move
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                #append move
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                            
        def Straight(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                pos_move_row = row + row_incr
                pos_move_col = col + col_incr
                
                while True:
                    if Square.in_range(pos_move_row, pos_move_col):
                        #create move square
                        initial = Square(row, col)
                        final_piece = self.squares[pos_move_row][pos_move_col].piece
                        final = Square(pos_move_row, pos_move_col, final_piece)
                        #pos move
                        move = Move(initial, final)
                    
                        #empty
                        if self.squares[pos_move_row][pos_move_col].isempty():
                            if bool:
                                if not self.in_check(piece, move):
                                    #append move
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                    
                        #rival
                        elif self.squares[pos_move_row][pos_move_col].has_rival(piece.color):
                            if bool:
                                if not self.in_check(piece, move):
                                    #append move
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            break
                        
                        #team
                        elif self.squares[pos_move_row][pos_move_col].has_team(piece.color):
                            break
                        
                    #not in range
                    else: break
                    
                    #increment
                    pos_move_row = pos_move_row + row_incr
                    pos_move_col = pos_move_col + col_incr
        def King_moves():
            adj = [
                (row-1, col+0),
                (row-1, col+1),
                (row-1, col-1),
                (row+1, col+0),
                (row+1, col+1),
                (row+1, col-1),
                (row+0, col-1),
                (row+0, col+1)
            ]
            
            #norm moves
            for pos_move in adj:
                pos_move_row, pos_move_col = pos_move
                if Square.in_range(pos_move_row, pos_move_col):
                    if self.squares[pos_move_row][pos_move_col].isempty_or_rival(piece.color):
                        #create squares of new move
                        initial = Square(row, col)
                        final = Square(pos_move_row, pos_move_col)
                        #create move
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                #append move
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        
            #castling
            if not piece.moved:
                #O-O-O
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece():
                                break #castling process stopped
                                
                            if c == 3:
                                piece.left_rook = left_rook
                                
                                #rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)
                                
                                #king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)
                                if bool:
                                    if (not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR)) and (not self.in_way(left_rook, moveR)):
                                        print(self.in_check(left_rook, moveR))
                                        #print('hi')
                                        left_rook.add_move(moveR)
                                        #append move
                                        piece.add_move(moveK)
                                        self.check_castle = True
                                        
                                else:
                                    left_rook.add_move(moveR)
                                    piece.add_move(moveK)
                                
                                        
                #O-O
                right_rook = self.squares[row][7].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece():
                                break #castling process stopped
                                
                            if c == 6:
                                piece.right_rook = right_rook
                                #rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)
                                
                                #king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)
                                if bool:
                                    if (not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR)) and (not self.in_way(right_rook, moveR)):
                                        #print('hi')
                                        right_rook.add_move(moveR)
                                        #append move
                                        piece.add_move(moveK)
                                        self.check_castle = True
                                        
                                else:
                                    right_rook.add_move(moveR)
                                    piece.add_move(moveK)
                                
        if isinstance(piece, Pawn): Pawn_moves()
        elif isinstance(piece, Knight): Knight_moves()
        elif isinstance(piece, Bishop): Straight(diagonal)
        elif isinstance(piece, Rook): Straight(straight)
        elif isinstance(piece, Queen): Straight(diagonal + straight)
        elif isinstance(piece, King): King_moves()
        
    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final
        
        en_passant_empty = self.squares[final.row][final.col].isempty()
        
        #console move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        
        
        #cool pawn moves
        if isinstance(piece, Pawn):
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                #console move update            
                self.squares[initial.row][initial.col+diff].piece = None
                self.squares[final.row][final.col].piece = piece
                if not testing:
                    sound = Sound(os.path.join('chess-AI/assets/sounds/capture.wav'))
                    sound.play()
                
        #promotion
        else:
            self.check_promotion(piece, final)
        
        #castling
        if self.check_castle:
            if isinstance(piece, King):
                if self.castling(initial, final):
                    diff = final.col - initial.col
                    rook = piece.left_rook if (diff < 0) else piece.right_rook
                    #print(rook.moves)
                    self.move(rook, rook.moves[-1])
        #move
        piece.moved = True
        
        #clear valid moves
        piece.clear_moves()
        
        #save last move
        self.last_move = move
        
    def valid_move(self, piece, move):
        if piece is not None:
            return move in piece.moves
        
    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            promotion = True
            while promotion:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.squares[final.row][final.col].piece = Queen(piece.color)
                            promotion = False
                        if event.key == pygame.K_r:
                            self.squares[final.row][final.col].piece = Rook(piece.color)
                            promotion = False
                        if event.key == pygame.K_b:
                            self.squares[final.row][final.col].piece = Bishop(piece.color)
                            promotion = False
                        if event.key == pygame.K_k:
                            self.squares[final.row][final.col].piece = Knight(piece.color)
                            promotion = False
            
    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2
    
    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)
        
        for row in range(rank):
            for col in range(file):
                if temp_board.squares[row][col].has_rival(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False
    
    def in_way(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)
        
        for row in range(rank):
            for col in range(file):
                if temp_board.squares[row][col].has_rival(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, Rook):
                            return True
        return False
        
    def set_true(self, piece):
        if not isinstance(piece, Pawn):
            return
        
        for row in range(rank):
            for col in range(file):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
        
        piece.en_passant = True
        
    def _create(self):        
        for row in range(rank):
            for col in range(file):    
                self.squares[row][col] = Square(row, col)

    def _add_piece(self, color):
        if color == 'white':
            row_pawn, row_other = (6, 7)
        else:
            row_pawn, row_other = (1, 0)
            
        #pawns
        for col in range(file):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color)) #all pawns
        
        #knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
        
        #bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
        
        #rooks
        self.squares[row_other][0] = Square(row_other, 2, Rook(color))
        self.squares[row_other][7] = Square(row_other, 5, Rook(color))
        
        #queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        
        #King
        self.squares[row_other][4] = Square(row_other, 4, King(color))