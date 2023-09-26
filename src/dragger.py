import pygame
from const import *

class Dragger:
    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_rank = 0
        self.initial_file = 0
    
    #blit method
    
    def update_blit(self, surface):
        if self.piece is not None:
            #texture
            self.piece.set_texture(size = 128) 
            texture = self.piece.texture
                #img
            img = pygame.image.load(texture)
                #rect
            img_center = (self.mouseX, self.mouseY)
            self.piece.texture_rect = img.get_rect(center=img_center)
                #blit
            surface.blit(img, self.piece.texture_rect)
            
        #other methods
    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos #(Xcood, Ycood)
        
    def save_initial(self, pos):
         self.initial_rank = pos[1] // SQSIZE
         self.initial_file = pos[0] // SQSIZE
        
    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True
        
    def undrag_piece(self):
        self.piece = None
        self.dragging = False