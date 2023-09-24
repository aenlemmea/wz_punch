import pygame as pg
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.wall_textures = self.load_wall_textures()
    
    def draw(self):
        self.render_game_objects()
    
    def render_game_objects(self):
        list_objects = sorted(self.game.raycast.objects_to_render, key= lambda  t: t[0], reverse=True )
        for depth, image, pos in list_objects:
            self.game.screen.blit(image, pos)
        
    @staticmethod
    def get_texture(path, size=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, size)
    
    def load_wall_textures(self):
        return {
                1: self.get_texture('assets/textures/256_Brick 01 Mud.png'),
                2: self.get_texture('assets/textures/256_Brick 02.png'),
                3: self.get_texture('assets/textures/256_Brick 03.png'),
                4: self.get_texture('assets/textures/256_Brick 04.png'),
                5: self.get_texture('assets/textures/256_Brick 05.png'),
            }