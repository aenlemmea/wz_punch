from sprite_object import *
     
class Staff(AnimatedSprite):
    def __init__(self, game, path='assets/weapon/staff/staff1.png', scale=2, anim_time=20):
        super().__init__(game=game, path=path, scale=scale)
        self.imager = deque(
                [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
                for img in self.images
                ])
        self.weapon_pos = (HALF_WIDTH - self.imager[0].get_width() // 2, (HEIGHT - self.imager[0].get_height() // 1.3))
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 50
    
    def animate_shot(self):
            if self.reloading:
                self.game.player.fire = False
                if self.anim_trig:
                    self.imager.rotate(-1)
                    self.image = self.imager[0]
                    self.frame_counter += 1
                    if self.frame_counter == self.num_images:
                        self.reloading = False
                        self.frame_counter = 0
    
    def draw(self):
        self.game.screen.blit(self.imager[0], self.weapon_pos)
    
    def update(self):
        self.check_anim_time()
        self.animate_shot()