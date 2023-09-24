from sprite_object import *

class SpriteHandler():
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.static_sprite_path = 'assets/sprites/static/'
        self.anim_sprite_path = 'assets/sprites/anim'
        add_sprite = self.add_sprite
        
        add_sprite(SpriteObject(game))
        add_sprite(AnimatedSprite(game))
    
    def update(self):
        [sprite.update() for sprite in self.sprite_list]
        
    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)