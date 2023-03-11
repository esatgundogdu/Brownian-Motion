import pygame
import math

FPS = 60
PIXEL_PER_METER = 40

class Brownian:
    def __init__(self, width=640, height=480):
        self.size = self.width, self.height = width, height

        pygame.display.set_caption("Brownian Motion")
        self.screen = pygame.display.set_mode(self.size)

        self.robot = _Robot(self.width/2, self.height/2)

        self.clock = pygame.time.Clock()
        self.done = False

    def start(self):
        while not self.done:
            # Limit 60fps
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            self.screen.fill("white")
            self.robot.draw(self.screen)

            pygame.display.flip()

class _Robot:
    def __init__(self, x, y):
        self.x, self.y, self.yaw = x, y, 0
        
        self.v = 1.0
        self.w = 0.5

        l = 4
        self.arrowPoints = [(0, l), (0, 2*l), (3*l, 2*l), (3*l, 3*l), (4*l, l*1.5), (l*3, 0), (l*3, l)] 
        self.arrowPoints = [(x+self.x, self.y+y-1.5*l) for (x,y) in self.arrowPoints]

    def draw(self, screen):
        pygame.draw.circle(screen, "blue", (self.x, self.y), 20)
        pygame.draw.polygon(screen, (255, 0, 50), self.arrowPoints)

        self.update()
        
    def update(self):
        # rotate
        d_angle = self.w / FPS
        
        self.yaw += d_angle
        if self.yaw > math.pi:
            self.yaw -= 2*math.pi

        for i, (x,y) in enumerate(self.arrowPoints):
            d_x = x - self.x
            d_y = y - self.y
            
            xr = d_x * math.cos(d_angle) - d_y * math.sin(d_angle)
            yr = d_x * math.sin(d_angle) + d_y * math.cos(d_angle)

            self.arrowPoints[i] = (self.x+xr, self.y+yr)
            
        # move
        d_shift = self.v / FPS * PIXEL_PER_METER 
        offsetX = d_shift * math.cos(self.yaw) 
        offsetY = d_shift * math.sin(self.yaw)

        self.x += offsetX
        self.y += offsetY

        self.arrowPoints = [(x+offsetX, y+offsetY) for (x, y) in self.arrowPoints]
        
if __name__ == "__main__":
    brownian = Brownian()
    brownian.start()
