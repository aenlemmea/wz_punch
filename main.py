import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycast import *
from object_renderer import *
from sprite_handler import *
from staff import *
from sound import *

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycast = RayCast(self)
        self.sprite_handler = SpriteHandler(self)
        self.staff = Staff(self)
        self.sound = Sound(self)

    def update(self):
        self.player.update()
        self.raycast.update()
        self.sprite_handler.update()
        self.staff.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        
    def draw(self):
        self.screen.fill('black')
        self.object_renderer.draw()
        self.staff.draw()
        #self.map.draw()
        #self.player.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
