from settings import *
import pygame as pg
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.fire = False
        self.diag_fix = 1 / math.sqrt(2)
    
    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.fire and not self.game.staff.reloading:
                self.game.sound.spell.play()
                self.fire = True
                self.game.staff.reloading = True

    def movement(self):
        sin_player = math.sin(self.angle)
        cos_player = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_player
        speed_cos = speed * cos_player

        keys = pg.key.get_pressed()
        kp = -1
        if keys[pg.K_w]:
                kp += 1
                dx += speed_cos
                dy += speed_sin
        if keys[pg.K_s]:
                kp += 1
                dx += -speed_cos
                dy += -speed_sin
        if keys[pg.K_d]:
                kp += 1
                dx += -speed_sin
                dy +=  speed_cos
        if keys[pg.K_a]:
                kp += 1
                dx += +speed_cos
                dy +=  speed_sin
        
        if kp:
            dx *= self.diag_fix
            dy *= self.diag_fix
        
        self.check_wall_collison(dx, dy)

        #if keys[pg.K_LEFT]:
        #    self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        #if keys[pg.K_RIGHT]:
        #    self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau # FOV within 2 * PI = tau.

    def check_wall(self, x, y):
        return (x,y) not in self.game.map.world_map
    
    def check_wall_collison(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy
        

    def draw(self):
        #pg.draw.line(self.game.screen, 'red', (self.x * 100, self.y * 100),
        #        (self.x * 100 + WIDTH * math.cos(self.angle),
        #         self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)
    
    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENS * self.game.delta_time

    def update(self):
        self.movement()
        self.mouse_control()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
