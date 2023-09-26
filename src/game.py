import pygame
from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square

class Game:
    def __init__ (self):
        self.next_player = 'white'
        self.hovered_sq = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()
    
    #renders
    def show_bg(self, surface):
        theme = self.config.theme
        
        for row in range(rank):
            for col in range(file):
                if (row + col) % 2 == 0:
                    color = theme.bg.light
                else:
                    color = theme.bg.dark
                
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                
                pygame.draw.rect(surface, color, rect)
                #show cood
                if col == 0:
                    #color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    #label
                    lbl = self.config.font.render(str(rank - row), 1, color)
                    lbl_pos = (5, 5 + row * SQSIZE)
                    #blit
                    surface.blit(lbl, lbl_pos)
                
                if row == 7:
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    #label
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    #blit
                    surface.blit(lbl, lbl_pos)
                
                
    def show_pieces(self, surface):
        for row in range(file):
            for col in range(rank):
                #piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    
                    #all but dragger
                    if piece != self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center = img_center)
                        surface.blit(img, piece.texture_rect)
                        
    def show_moves(self, surface):
        theme = self.config.theme
        
        if self.dragger.dragging:
            piece = self.dragger.piece
            
            #loop all valid moves
            if  piece is not None:
                for move in piece.moves:
                    #color
                    color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                    #rect
                    rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                    #blit
                    pygame.draw.rect(surface, color, rect)
    def show_last(self, surface):
        theme = self.config.theme
        
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            
            for pos in [initial, final]:
                #color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                #rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                #blit
                pygame.draw.rect(surface, color, rect)
                
    def show_hover(self, surface):
        if self.hovered_sq:
            #color
            color = (180, 180, 180)
            #rect
            rect = (self.hovered_sq.col * SQSIZE, self.hovered_sq.row * SQSIZE, SQSIZE, SQSIZE)
            #blit
            pygame.draw.rect(surface, color, rect, width=3)
                    
    #other methods
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'
    
    def set_hover(self, row, col):
        if row < 8 and col > 0:
            self.hovered_sq = self.board.squares[row][col]
        
    def change_theme(self):
        self.config.change_theme()
    
    def sound_effect(self, capture = False):
        if capture:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
    
    def reset(self):
        self.__init__()