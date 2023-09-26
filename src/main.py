#imports
import pygame, sys
from const import *
from game import Game
from square import Square
from move import Move

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess(I think)')
        self.game = Game()
            
    def mainloop(self):
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        
        while True:
            game.show_bg(screen)
            game.show_last(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)
            
            if dragger.dragging:
                dragger.update_blit(screen)
            
            for event in pygame.event.get():
                #click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    
                    clicked_rank = dragger.mouseY // SQSIZE
                    clicked_file = dragger.mouseX // SQSIZE
                    
                    #if square has a piece
                    if board.squares[clicked_rank][clicked_file].has_piece:                        
                        piece = board.squares[clicked_rank][clicked_file].piece
                        
                        #valid moves color
                        if piece is not None:
                            if piece.color == game.next_player:
                                board.calc_moves(piece, clicked_rank, clicked_file, bool=True)
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)
                        
                        #show methods
                        game.show_bg(screen)
                        game.show_last(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                
                #mouse function
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    
                    game.set_hover(motion_row, motion_col)
                    
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        #show methods
                        game.show_bg(screen)
                        game.show_last(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                
                #click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE
                        
                        #create possible move
                        initial = Square(dragger.initial_rank, dragger.initial_file)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)
                        
                        #valid?
                        if board.valid_move(dragger.piece, move):
                            #normal
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece,move)
                            
                            board.set_true(dragger.piece)
                            #sound
                            game.sound_effect(captured)
                            #show methods
                            game.show_bg(screen)
                            game.show_last(screen)
                            game.show_pieces(screen)
                            #next turn
                            game.next_turn()
                            
                    
                    dragger.undrag_piece()
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        game.change_theme()
                    
                    if event.key == pygame.K_ESCAPE:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                
                #quit app
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

main = Main()
main.mainloop()