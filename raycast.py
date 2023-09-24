import pygame as pg
from settings import *
import math

class RayCast:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, projected_height, texture, offset = values
            
            if projected_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(offset * (TEXTURE_SIZE - SCALE),
                                                                0, SCALE, TEXTURE_SIZE)
                wall_column = pg.transform.scale(wall_column, (SCALE, projected_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - projected_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / projected_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE),  HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))
            
    def ray_cast(self):
        self.ray_casting_result = []
        px, py = self.game.player.pos # player pos (can be within gridlines)
        x_map, y_map = self.game.player.map_pos # map pos (fixed grid)
        
        texture_vert, texture_hort = 1, 1
        
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS):
            sin_r = math.sin(ray_angle)
            cos_r = math.cos(ray_angle)
            
            # x axis
            y_hort, dy = (y_map + 1, 1) if sin_r > 0 else (y_map - 1e-6, -1)
            
            depth_hort = (y_hort - py) / sin_r
            x_hort = px + depth_hort * cos_r
            
            delta_depth = dy / sin_r
            dx = delta_depth * cos_r
            
            for i in range(MAX_DEPTH):
                tile_hit_hort = int(x_hort), int(y_hort)
                if tile_hit_hort in self.game.map.world_map:
                    texture_hort = self.game.map.world_map[tile_hit_hort]
                    break
                x_hort += dx
                y_hort += dy
                depth_hort += delta_depth
            
            
            # y axis hits
            x_vert, dx = (x_map + 1, 1) if cos_r > 0 else (x_map - 1e-6, -1)
            
            depth_vert = (x_vert - px) / cos_r
            y_vert = py + depth_vert * sin_r
            
            delta_depth = dx / cos_r
            dy = delta_depth * sin_r
            
            for i in range(MAX_DEPTH):
                tile_hit_vert = int(x_vert), int(y_vert)
                if tile_hit_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_hit_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth
                
            # depth, texture offset
            if depth_vert < depth_hort:
                depth, texture  = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_r > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hort, texture_hort
                x_hort %= 1
                offset = (1 - x_hort) if sin_r > 0 else x_hort
            
            # remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)
            
            projected_height = SCREEN_DIST / (depth + 0.0001)
            
            self.ray_casting_result.append((depth, projected_height, texture, offset))
            
            ray_angle += DELTA_ANGLE
    
    def draw_blank_torch(self, px, py, depth, cos_r, sin_r):
        pg.draw.line(self.game.screen, 'yellow', (100 * px, 100 * py),
                     (100 * px + 100 * depth * cos_r, 100 * py + 100 * depth * sin_r),
                     2
                     )
        
    def draw_blank_walls(self, projected_height, ray, depth):
        color = [255 / (1 + depth ** 5 * 0.0002)] * 3
        pg.draw.rect(self.game.screen, color,
                     (ray * SCALE, HALF_HEIGHT - projected_height // 2, SCALE, projected_height))
    
    def update(self):
        self.ray_cast()
        self.get_objects_to_render()